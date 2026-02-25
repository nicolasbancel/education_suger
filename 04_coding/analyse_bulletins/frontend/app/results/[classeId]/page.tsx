"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams, useSearchParams, useRouter } from "next/navigation";

interface Student {
  id: string;
  first_name: string;
  last_name: string;
  ecoledirecte_id: string;
}

interface BulletinLine {
  id: string;
  subject: string;
  appreciation: string | null;
  contenu: string | null;
  average: number | null;
  average_class: number | null;
  average_min: number | null;
  average_max: number | null;
  rang: number | null;
  absences: number | null;
  tardiness: number | null;
}

interface LLMOutput {
  id: string;
  general_appreciation: string | null;
  synthesis: string | null;
  reward_suggestion: string | null;
  manually_edited: boolean;
}

interface StudentWithData {
  student: Student;
  bulletin_lines: BulletinLine[];
  llm_output: LLMOutput | null;
}

interface JobStatus {
  job_id: string;
  status: string;
  progress: number;
  total: number;
  errors: string[];
}

const REWARD_OPTIONS = [
  "Félicitations",
  "Tableau d'honneur",
  "Encouragements",
  "Mention neutre",
  "Aucune",
];

export default function ResultsPage() {
  const { classeId } = useParams<{ classeId: string }>();
  const searchParams = useSearchParams();
  const router = useRouter();
  const trimestre = Number(searchParams.get("trimestre") || 1);
  const token = typeof window !== "undefined" ? localStorage.getItem("session_token") : null;

  const [results, setResults] = useState<StudentWithData[]>([]);
  const [job, setJob] = useState<JobStatus | null>(null);
  const [downloading, setDownloading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [defaultPrompt, setDefaultPrompt] = useState("");
  const [customPrompt, setCustomPrompt] = useState("");
  const [showPrompt, setShowPrompt] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValues, setEditValues] = useState<Partial<LLMOutput>>({});
  const [generateError, setGenerateError] = useState<string>("");
  const [expandedStudents, setExpandedStudents] = useState<Set<string>>(new Set());

  const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };

  const fetchResults = useCallback(async () => {
    const res = await fetch(`/api/llm/outputs/${classeId}?trimestre=${trimestre}`, { headers });
    if (res.ok) setResults(await res.json());
  }, [classeId, trimestre]);

  useEffect(() => {
    if (!token) { router.push("/"); return; }
    fetchResults();
    fetch("/api/llm/default-prompt", { headers })
      .then((r) => r.json())
      .then((d) => { setDefaultPrompt(d.prompt); setCustomPrompt(d.prompt); });
  }, [token, fetchResults]);

  // Polling job status
  useEffect(() => {
    if (!job || job.status !== "running") return;
    const interval = setInterval(async () => {
      const res = await fetch(`/api/bulletins/jobs/${job.job_id}`, { headers });
      if (res.ok) {
        const updated: JobStatus = await res.json();
        setJob(updated);
        if (updated.status !== "running") {
          clearInterval(interval);
          setDownloading(false);
          fetchResults();
        }
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [job, fetchResults]);

  async function startDownload() {
    setDownloading(true);
    const res = await fetch(`/api/bulletins/fetch/${classeId}?trimestre=${trimestre}`, {
      method: "POST",
      headers,
    });
    if (res.ok) setJob(await res.json());
    else setDownloading(false);
  }

  async function generateAll() {
    setGenerating(true);
    setGenerateError("");
    const studentIds = results.map((r) => r.student.id);
    const res = await fetch("/api/llm/generate", {
      method: "POST",
      headers,
      body: JSON.stringify({ student_ids: studentIds, trimestre, custom_prompt: customPrompt }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Erreur inconnue" }));
      const detail = Array.isArray(err.detail) ? err.detail.join("\n") : err.detail;
      setGenerateError(detail || "La génération a échoué");
    }
    await fetchResults();
    setGenerating(false);
  }

  function toggleExpand(studentId: string) {
    setExpandedStudents((prev) => {
      const next = new Set(prev);
      if (next.has(studentId)) next.delete(studentId);
      else next.add(studentId);
      return next;
    });
  }

  async function saveEdit(outputId: string) {
    await fetch(`/api/llm/outputs/${outputId}`, {
      method: "PATCH",
      headers,
      body: JSON.stringify(editValues),
    });
    setEditingId(null);
    fetchResults();
  }

  const hasData = results.some((r) => r.bulletin_lines.length > 0);
  const hasOutputs = results.some((r) => r.llm_output);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <button onClick={() => router.push("/classes")} className="text-sm text-gray-500 hover:text-gray-700 mb-1">
            ← Retour aux classes
          </button>
          <h2 className="text-xl font-semibold text-gray-800">
            Trimestre {trimestre} — {results.length} élève{results.length > 1 ? "s" : ""}
          </h2>
        </div>
        <div className="flex gap-2">
          {hasOutputs && (
            <>
              <a
                href={`/api/export/${classeId}/csv?trimestre=${trimestre}`}
                className="border rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                Export CSV
              </a>
              <a
                href={`/api/export/${classeId}/docx?trimestre=${trimestre}`}
                className="border rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                Export DOCX
              </a>
              <a
                href={`/api/export/${classeId}/pdf?trimestre=${trimestre}`}
                className="border rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                Export PDF
              </a>
            </>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="bg-white border rounded-xl p-4 mb-6 flex flex-wrap gap-3 items-center">
        <button
          onClick={startDownload}
          disabled={downloading}
          className="bg-gray-800 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-gray-900 disabled:opacity-50"
        >
          {downloading
            ? job
              ? `Téléchargement… ${job.progress}/${job.total}`
              : "Démarrage…"
            : "1. Récupérer les bulletins"}
        </button>

        <button
          onClick={generateAll}
          disabled={generating || !hasData}
          className="bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {generating ? "Génération en cours…" : "2. Générer les appréciations (LLM)"}
        </button>

        <button
          onClick={() => setShowPrompt(!showPrompt)}
          className="border rounded-lg px-4 py-2 text-sm text-gray-600 hover:bg-gray-50"
        >
          {showPrompt ? "Masquer le prompt" : "Configurer le prompt"}
        </button>
      </div>

      {/* Generate error */}
      {generateError && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-800">
          <strong>Erreur de génération :</strong>
          <pre className="mt-1 whitespace-pre-wrap">{generateError}</pre>
        </div>
      )}

      {/* Job errors */}
      {job?.errors && job.errors.length > 0 && (
        <div className="mb-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm text-yellow-800">
          <strong>Avertissements :</strong>
          <ul className="mt-1 list-disc list-inside">
            {job.errors.map((e, i) => <li key={i}>{e}</li>)}
          </ul>
        </div>
      )}

      {/* Prompt editor */}
      {showPrompt && (
        <div className="mb-6 bg-white border rounded-xl p-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Prompt de génération
          </label>
          <textarea
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            rows={5}
            className="w-full border rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={() => setCustomPrompt(defaultPrompt)}
            className="mt-2 text-xs text-gray-500 hover:text-gray-700"
          >
            Réinitialiser au prompt par défaut
          </button>
        </div>
      )}

      {/* Results table */}
      {results.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          Aucun élève trouvé. Synchronisez d&apos;abord les élèves depuis la page des classes.
        </div>
      ) : (
        <div className="space-y-4">
          {results.map(({ student, bulletin_lines, llm_output }) => (
            <div key={student.id} className="bg-white border rounded-xl p-5">
              <div className="flex items-start justify-between">
                <div>
                  <span className="font-semibold text-gray-800">
                    {student.last_name} {student.first_name}
                  </span>
                  {llm_output?.manually_edited && (
                    <span className="ml-2 text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full">
                      modifié
                    </span>
                  )}
                  {bulletin_lines.length > 0 && (
                    <button
                      onClick={() => toggleExpand(student.id)}
                      className="ml-2 text-xs text-blue-500 hover:text-blue-700 underline"
                    >
                      {expandedStudents.has(student.id) ? "Masquer bulletin" : `Voir bulletin (${bulletin_lines.length} matières)`}
                    </button>
                  )}
                </div>

                {llm_output && editingId !== llm_output.id && (
                  <button
                    onClick={() => {
                      setEditingId(llm_output.id);
                      setEditValues({
                        general_appreciation: llm_output.general_appreciation || "",
                        synthesis: llm_output.synthesis || "",
                        reward_suggestion: llm_output.reward_suggestion || "",
                      });
                    }}
                    className="text-xs text-gray-500 hover:text-gray-700 border rounded px-2 py-1"
                  >
                    Modifier
                  </button>
                )}
              </div>

              {/* Données bulletin (expandable) */}
              {expandedStudents.has(student.id) && bulletin_lines.length > 0 && (
                <div className="mt-3 border-t pt-3">
                  {bulletin_lines.filter(l => l.subject === "BILAN").map(bilan => (
                    <div key={bilan.id} className="mb-3 bg-blue-50 rounded-lg px-3 py-2 text-sm">
                      <span className="font-medium text-blue-700">Bilan général</span>
                      {bilan.average && <span className="ml-2 text-blue-600 font-semibold">{bilan.average}/20</span>}
                      {bilan.appreciation && <p className="mt-1 text-gray-700 italic">{bilan.appreciation}</p>}
                      {(bilan.absences ?? 0) > 0 && <span className="mt-1 block text-xs text-orange-600">{bilan.absences} absence(s) · {bilan.tardiness ?? 0} retard(s)</span>}
                    </div>
                  ))}
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="text-gray-500 border-b">
                        <th className="text-left py-1 font-medium">Matière</th>
                        <th className="text-right py-1 font-medium w-12">Élève</th>
                        <th className="text-right py-1 font-medium w-12">Classe</th>
                        <th className="text-right py-1 font-medium w-20">Min – Max</th>
                        <th className="text-left py-1 font-medium pl-3">Appréciation</th>
                      </tr>
                    </thead>
                    <tbody>
                      {bulletin_lines.filter(l => l.subject !== "BILAN").map(line => (
                        <tr key={line.id} className="border-b border-gray-50 align-top">
                          <td className="py-1 text-gray-700 font-medium">{line.subject}</td>
                          <td className="text-right py-1 font-semibold text-gray-800">{line.average ?? "—"}</td>
                          <td className="text-right py-1 text-gray-500">{line.average_class ?? "—"}</td>
                          <td className="text-right py-1 text-gray-400">
                            {line.average_min != null && line.average_max != null
                              ? `${line.average_min} – ${line.average_max}`
                              : "—"}
                          </td>
                          <td className="pl-3 py-1 text-gray-600">
                            {line.appreciation && <p>{line.appreciation}</p>}
                            {line.contenu && <p className="text-gray-400 italic mt-0.5">{line.contenu}</p>}
                            {!line.appreciation && !line.contenu && <span className="text-gray-300">—</span>}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {llm_output ? (
                editingId === llm_output.id ? (
                  <div className="mt-3 space-y-3">
                    <div>
                      <label className="text-xs font-medium text-gray-600">Appréciation générale</label>
                      <textarea
                        value={editValues.general_appreciation || ""}
                        onChange={(e) => setEditValues({ ...editValues, general_appreciation: e.target.value })}
                        rows={3}
                        className="w-full mt-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Synthèse</label>
                      <textarea
                        value={editValues.synthesis || ""}
                        onChange={(e) => setEditValues({ ...editValues, synthesis: e.target.value })}
                        rows={3}
                        className="w-full mt-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-600">Récompense</label>
                      <select
                        value={editValues.reward_suggestion || ""}
                        onChange={(e) => setEditValues({ ...editValues, reward_suggestion: e.target.value })}
                        className="mt-1 border rounded-lg px-3 py-2 text-sm w-full"
                      >
                        {REWARD_OPTIONS.map((o) => <option key={o}>{o}</option>)}
                      </select>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => saveEdit(llm_output.id)}
                        className="bg-blue-600 text-white rounded-lg px-3 py-1.5 text-sm hover:bg-blue-700"
                      >
                        Enregistrer
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="border rounded-lg px-3 py-1.5 text-sm hover:bg-gray-50"
                      >
                        Annuler
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="text-xs font-medium text-gray-500 mb-1">Appréciation générale</div>
                      <p className="text-gray-700">{llm_output.general_appreciation}</p>
                    </div>
                    <div>
                      <div className="text-xs font-medium text-gray-500 mb-1">Synthèse</div>
                      <p className="text-gray-700 whitespace-pre-line">{llm_output.synthesis}</p>
                    </div>
                    <div>
                      <div className="text-xs font-medium text-gray-500 mb-1">Récompense</div>
                      <span className="inline-block bg-blue-50 text-blue-700 px-2 py-1 rounded-full text-xs font-medium">
                        {llm_output.reward_suggestion}
                      </span>
                    </div>
                  </div>
                )
              ) : (
                <div className="mt-2 text-sm text-gray-400">
                  {bulletin_lines.length > 0
                    ? "Bulletin extrait — cliquez sur « Générer » pour obtenir les appréciations"
                    : "Pas encore de données — téléchargez les bulletins d'abord"}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
