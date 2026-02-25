"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Classe {
  id: string;
  name: string;
  ecoledirecte_id: string;
  annee_scolaire: string;
}

function useAuth() {
  const token = typeof window !== "undefined" ? localStorage.getItem("session_token") : null;
  return token;
}

export default function ClassesPage() {
  const router = useRouter();
  const token = useAuth();
  const [classes, setClasses] = useState<Classe[]>([]);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState("");
  const [selectedTrimestre, setSelectedTrimestre] = useState(1);

  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (!token) { router.push("/"); return; }
    fetchClasses();
  }, [token]);

  async function fetchClasses() {
    const res = await fetch("/api/ecoledirecte/classes", { headers });
    if (res.ok) setClasses(await res.json());
  }

  async function syncClasses() {
    setSyncing(true);
    setError("");
    try {
      const res = await fetch("/api/ecoledirecte/sync-classes", {
        method: "POST",
        headers,
      });
      if (!res.ok) throw new Error((await res.json()).detail);
      setClasses(await res.json());
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setSyncing(false);
    }
  }

  async function selectClasse(classe: Classe) {
    // Sync students then navigate to results
    const res = await fetch(`/api/ecoledirecte/classes/${classe.id}/sync-students`, {
      method: "POST",
      headers,
    });
    if (!res.ok) {
      setError("Impossible de synchroniser les élèves");
      return;
    }
    router.push(`/results/${classe.id}?trimestre=${selectedTrimestre}`);
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-800">Mes classes</h2>
        <div className="flex items-center gap-3">
          <select
            value={selectedTrimestre}
            onChange={(e) => setSelectedTrimestre(Number(e.target.value))}
            className="border rounded-lg px-3 py-2 text-sm"
          >
            <option value={1}>Trimestre 1</option>
            <option value={2}>Trimestre 2</option>
            <option value={3}>Trimestre 3</option>
          </select>
          <button
            onClick={syncClasses}
            disabled={syncing}
            className="bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {syncing ? "Synchronisation…" : "Synchroniser depuis EcoleDirecte"}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 text-sm text-red-600 bg-red-50 rounded-lg px-4 py-2">
          {error}
        </div>
      )}

      {classes.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <p>Aucune classe trouvée.</p>
          <p className="text-sm mt-1">Cliquez sur &quot;Synchroniser depuis EcoleDirecte&quot; pour commencer.</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {classes.map((c) => (
            <button
              key={c.id}
              onClick={() => selectClasse(c)}
              className="bg-white border rounded-xl p-6 text-left hover:border-blue-400 hover:shadow-sm transition-all group"
            >
              <div className="text-lg font-semibold text-gray-800 group-hover:text-blue-600">
                {c.name}
              </div>
              <div className="text-sm text-gray-500 mt-1">{c.annee_scolaire}</div>
              <div className="mt-3 text-xs text-blue-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                Préparer le trimestre {selectedTrimestre} →
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
