"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  PenTool,
  CheckCircle,
  Loader2,
  ChevronRight,
  GraduationCap,
  Sparkles,
  BookOpen,
  LayoutDashboard,
  FileText,
  Terminal,
  Download,
  Copy,
  Plus
} from "lucide-react";
import ReactMarkdown from 'react-markdown';

export default function LingoAcademicPremium() {
  const [inputText, setInputText] = useState("");
  const [status, setStatus] = useState("idle"); // idle, processing, completed, error
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("Ready to start your research.");
  const [result, setResult] = useState("");
  const [logs, setLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (status === "processing") {
      interval = setInterval(async () => {
        try {
          const res = await fetch("http://localhost:8000/status");
          const data = await res.json();

          if (data.status === "processing") {
            setMessage(data.message);
            setProgress(data.progress || 20);
            if (data.message && !logs.includes(data.message)) {
              setLogs(prev => [...prev, data.message]);
            }
          } else if (data.status === "completed") {
            setStatus("completed");
            setResult(data.result);
            setProgress(100);
            setMessage("Research Completed Successfully.");
            clearInterval(interval);
          } else if (data.status === "error") {
            setStatus("error");
            setMessage(data.message);
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 2000);
    }

    return () => clearInterval(interval);
  }, [status, logs]);

  const handleSubmit = async () => {
    if (!inputText) return;

    setStatus("processing");
    setProgress(10);
    setLogs(["Initializing pipeline..."]);
    setResult("");

    try {
      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      if (!res.ok) throw new Error("Failed to start process");

    } catch (err) {
      setStatus("error");
      setMessage("Connection to backend failed. Please ensure your Python server is running.");
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans selection:bg-primary/10 relative overflow-hidden">

      {/* Background Subtle Gradient */}
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_top_right,rgba(99,102,241,0.02),transparent)] pointer-events-none" />

      {/* Navigation / Header */}
      <nav className="border-b border-slate-200 bg-white/60 backdrop-blur-2xl sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary to-secondary p-1.5 rounded-lg">
              <GraduationCap className="text-white w-5 h-5" />
            </div>
            <span className="text-lg font-bold tracking-tight text-slate-900">LingoAcademic <span className="text-primary font-light">PRO</span></span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={() => setStatus("idle")} className="text-xs text-slate-500 hover:text-slate-900 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-full hover:bg-slate-100">
              <Plus className="w-3.5 h-3.5" />
              New Session
            </button>
            <div className="h-4 w-px bg-slate-200" />
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${status === "processing" ? "bg-amber-500 animate-pulse" : status === "idle" ? "bg-green-500" : "bg-primary"}`} />
              <span className="text-[10px] uppercase tracking-widest font-bold text-slate-400">{status}</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto p-6 lg:p-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* LEFT COLUMN: Controls & Input (Fixed-ish) */}
          <div className="lg:col-span-4 space-y-6">

            {/* Input Card */}
            <section className="glass rounded-[2rem] p-8 space-y-6 relative overflow-hidden group border border-slate-200/50">
              <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity text-slate-800">
                <LayoutDashboard className="w-32 h-32" />
              </div>

              <div className="relative z-10">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-2 text-slate-900">
                  <BookOpen className="w-6 h-6 text-primary" />
                  Research Input
                </h2>
                <p className="text-sm text-slate-500 mb-6 font-medium">Describe your research in English. LingoAcademic will handle the German translation.</p>

                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  disabled={status === "processing"}
                  placeholder="Enter your research prompt..."
                  className="w-full h-56 bg-white border border-slate-200 rounded-2xl p-5 text-sm leading-relaxed text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary/30 transition-all resize-none shadow-sm"
                />

                <button
                  onClick={handleSubmit}
                  disabled={!inputText || status === "processing"}
                  className="w-full mt-6 bg-primary hover:bg-primary/90 disabled:opacity-30 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all transform hover:translate-y-[-2px] active:translate-y-[0px] shadow-lg shadow-primary/20"
                >
                  {status === "processing" ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Generate Academic Paper
                    </>
                  )}
                </button>
              </div>
            </section>

            {/* Workflow Card */}
            <section className="glass rounded-[2rem] p-8 border border-slate-200/50">
              <h3 className="text-[10px] font-bold uppercase tracking-[0.25em] text-slate-400 mb-8">Agentic Pipeline</h3>
              <div className="space-y-8 relative">
                {/* Vertical line connector */}
                <div className="absolute left-6 top-6 bottom-6 w-px bg-slate-200" />

                <WorkflowStep
                  icon={<Search className="w-4 h-4" />}
                  title="The Librarian"
                  desc="Searching German sources"
                  status={progress > 30 ? "done" : progress > 10 ? "loading" : "pending"}
                />
                <WorkflowStep
                  icon={<PenTool className="w-4 h-4" />}
                  title="Academic Writer"
                  desc="Drafting & Grounding"
                  status={progress > 70 ? "done" : progress > 40 ? "loading" : "pending"}
                />
                <WorkflowStep
                  icon={<CheckCircle className="w-4 h-4" />}
                  title="Native Critic"
                  desc="Validating standards"
                  status={progress === 100 ? "done" : progress > 80 ? "loading" : "pending"}
                />
              </div>

              <div className="mt-10 pt-8 border-t border-slate-100">
                <div className="flex justify-between items-end mb-2">
                  <span className="text-[10px] uppercase font-bold text-primary tracking-widest">{message}</span>
                  <span className="text-2xl font-black text-slate-900">{progress}%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    className="h-full bg-gradient-to-r from-primary to-secondary"
                  />
                </div>
              </div>
            </section>
          </div>

          {/* RIGHT COLUMN: Output & Logs */}
          <div className="lg:col-span-8 flex flex-col gap-6">

            {/* Results Area */}
            <div className={`flex-1 min-h-[600px] glass rounded-[2.5rem] p-2 flex flex-col transition-all duration-700 ${status === "idle" ? "opacity-30 grayscale" : "opacity-100"} border border-slate-200/50`}>
              <div className="flex items-center justify-between p-6 pb-2">
                <div className="flex items-center gap-3 text-slate-900">
                  <FileText className="text-secondary w-5 h-5" />
                  <h2 className="text-xl font-semibold">Final Specification</h2>
                </div>
                <div className="flex gap-2 text-slate-400">
                  <button className="p-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 transition-colors tooltip" title="Copy to clipboard">
                    <Copy className="w-4 h-4" />
                  </button>
                  <button className="p-2.5 rounded-xl bg-primary/10 text-primary hover:bg-primary/20 transition-colors">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="flex-1 m-4 rounded-[2rem] bg-white border border-slate-100 p-10 overflow-auto scroll-smooth custom-scrollbar relative shadow-sm">
                <AnimatePresence mode="wait">
                  {status === "completed" ? (
                    <motion.div
                      key="result"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="prose prose-slate prose-blue max-w-none prose-sm"
                    >
                      <ReactMarkdown>{result}</ReactMarkdown>
                    </motion.div>
                  ) : status === "processing" ? (
                    <motion.div
                      key="waiting"
                      className="h-full flex flex-col items-center justify-center text-center opacity-40 py-20"
                    >
                      <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
                      <p className="text-lg font-semibold text-slate-800">Processing Research...</p>
                      <p className="text-sm text-slate-500">LingoAcademic agents are working at full speed.</p>
                    </motion.div>
                  ) : (
                    <div key="idle" className="h-full flex flex-col items-center justify-center text-center py-20">
                      <div className="bg-slate-50 p-6 rounded-full mb-6">
                        <GraduationCap className="w-12 h-12 text-slate-300" />
                      </div>
                      <p className="text-lg font-medium text-slate-400 font-serif italic">Clean academic output will appear here</p>
                    </div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* Bottom logs / Console Area */}
            <div className="h-48 glass rounded-[2rem] p-6 flex flex-col overflow-hidden border border-slate-200/50 bg-white/40">
              <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.25em] text-slate-400 mb-4 px-2">
                <Terminal className="w-3.5 h-3.5" />
                System Output
              </div>
              <div className="flex-1 overflow-y-auto space-y-1 pr-4 custom-scrollbar px-2 font-mono text-[11px]">
                {logs.length === 0 && <span className="text-slate-300 italic">No activity detected...</span>}
                {logs.map((log, i) => (
                  <div key={i} className="flex items-start gap-3 py-1 group">
                    <span className="text-slate-300 group-hover:text-primary transition-colors shrink-0">{new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' })}</span>
                    <span className="text-slate-500 group-hover:text-slate-800 transition-colors tracking-tight font-medium uppercase">{log}</span>
                  </div>
                ))}
                {status === "processing" && (
                  <div className="flex items-center gap-2 text-primary">
                    <span className="animate-pulse">_</span>
                    <span>Pending response from LLM engine...</span>
                  </div>
                )}
                <div ref={scrollRef} />
              </div>
            </div>

          </div>
        </div>
      </main>

      <style jsx global>{`
        .glass {
          background: rgba(255, 255, 255, 0.4);
          backdrop-filter: blur(24px);
          -webkit-backdrop-filter: blur(24px);
          border: 1px solid rgba(0, 0, 0, 0.04);
          box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.05);
        }
        .custom-scrollbar::-webkit-scrollbar {
          width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #e2e8f0;
          border-radius: 10px;
        }
        .gradient-text {
          background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .animate-glow {
           box-shadow: 0 0 40px rgba(79, 70, 229, 0.05);
        }
      `}</style>
    </div>
  );
}

function WorkflowStep({ icon, title, desc, status }: { icon: any, title: string, desc: string, status: "pending" | "loading" | "done" }) {
  return (
    <div className={`flex items-start gap-4 transition-all duration-700 relative z-10 ${status === "pending" ? "opacity-30" : "opacity-100"}`}>
      <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 shadow-sm border ${status === "done" ? "bg-green-50 text-green-600 border-green-100" : status === "loading" ? "bg-primary text-white border-primary/20 animate-pulse" : "bg-white text-slate-400 border-slate-100"}`}>
        {status === "loading" ? <Loader2 className="w-5 h-5 animate-spin" /> : icon}
      </div>
      <div className="pt-1.5 flex-1 p-3 rounded-2xl border border-transparent transition-all">
        <h4 className="font-bold text-slate-800 flex items-center gap-2">
          {title}
          {status === "done" && <CheckCircle className="w-3.5 h-3.5" />}
        </h4>
        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">{desc}</p>
      </div>
    </div>
  );
}
