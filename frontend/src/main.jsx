import React, { Component, Suspense, lazy, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowUpRight,
  BrainCircuit,
  Database,
  Github,
  Linkedin,
  Mail,
  MapPin,
  Network,
  Phone,
  Rocket,
  Sparkles,
  Terminal,
  Trophy,
  WandSparkles,
} from "lucide-react";
import { fallbackProfile } from "./data";
import "./styles.css";

const API_URL = "http://127.0.0.1:8000/api/profile";
const NeuralScene = lazy(() => import("./NeuralScene.jsx"));

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    console.error("Portfolio render failed:", error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="fallback-page">
          <h1>Arya Lolusare</h1>
          <p>Portfolio is loading. Refresh once, or restart the Vite dev server if this keeps showing.</p>
          <a className="button primary" href="https://github.com/AryaLolusare2712" target="_blank" rel="noreferrer">
            Open GitHub <ArrowUpRight size={18} />
          </a>
        </main>
      );
    }

    return this.props.children;
  }
}

function Pill({ children }) {
  return <span className="pill">{children}</span>;
}

function Section({ eyebrow, title, children, id }) {
  return (
    <section className="section" id={id}>
      <div className="section-heading">
        <span>{eyebrow}</span>
        <h2>{title}</h2>
      </div>
      {children}
    </section>
  );
}

const workflow = [
  {
    icon: BrainCircuit,
    title: "Model logic",
    text: "Prompt contracts, function calling, evaluation loops, and Gemini-first workflows.",
  },
  {
    icon: Database,
    title: "Retrieval layer",
    text: "Chunking, semantic reranking, FAISS search, and grounded responses for long documents.",
  },
  {
    icon: Network,
    title: "Agent systems",
    text: "Role-based agent graphs with research, coding, critique, synthesis, and visualized flow.",
  },
  {
    icon: Rocket,
    title: "Product surface",
    text: "FastAPI, Streamlit, Gradio, dashboards, and deployable experiences people can use.",
  },
];

const skillMeta = {
  "LLM & GenAI": {
    icon: BrainCircuit,
    focus: "I design grounded AI flows for contracts, careers, finance, and multi-step problem solving.",
    level: 94,
  },
  "ML / DL": {
    icon: Sparkles,
    focus: "I turn text and tabular signals into rankings, similarity scores, and recommendations.",
    level: 84,
  },
  "Backend & Tools": {
    icon: Rocket,
    focus: "I package models into usable APIs, dashboards, demos, and recruiter-ready product flows.",
    level: 88,
  },
  Data: {
    icon: Database,
    focus: "I shape datasets, vector search, charts, and live market feeds into useful interfaces.",
    level: 80,
  },
};

const projectExtras = {
  "CareerLens AI": {
    live: "https://careerlens-ai-mvp.streamlit.app/",
    problem: "Students need better-fit opportunities, while recruiters need faster candidate screening.",
    approach: "Resume parsing, semantic matching, skill-gap insights, recruiter search, shortlist boards, and AI summaries.",
    result: "A role-based career platform that connects student profiles to jobs, internships, and recruiter workflows.",
    architecture: ["Resume Upload", "Parse Skills", "FAISS Match", "Gemini Summary", "Recruiter Portal"],
  },
  LexAI: {
    live: "https://lexai-legalcontractanalyzer-u3jyuhvkz2xhzg4uqfjc69.streamlit.app/",
    problem: "Legal contracts are slow to review and risky clauses are easy to miss.",
    approach: "Gemini-powered structured analysis with risk scoring, clause flags, benchmark checks, and dashboard outputs.",
    result: "A contract intelligence tool that turns dense legal text into actionable review insights.",
    architecture: ["Contract Text", "Prompt Contract", "Gemini JSON", "Risk Score", "Insights Tabs"],
  },
  "Multi-Agent Problem Solver": {
    live: "https://huggingface.co/spaces/Arya0912/Multi-Agent-Problem-Solver",
    problem: "Complex prompts need planning, research, coding, and critique instead of one-shot answers.",
    approach: "Four Gemini-powered agents coordinate through role-specific tasks and a NetworkX workflow view.",
    result: "A deployed Hugging Face app that breaks down problems and synthesizes stronger final answers.",
    architecture: ["User Problem", "CEO Plan", "Research Agent", "Coder Agent", "Critic Review"],
  },
  FinPilot: {
    live: "https://finpilot-aiportfoliotracker.streamlit.app/",
    problem: "Investors need one place to track stocks, crypto, news, P&L, and AI analysis.",
    approach: "Streamlit dashboard with yfinance, CoinGecko, Plotly charts, Gemini analysis, and chat assistant.",
    result: "A live portfolio tracker for NSE/BSE stocks and 300+ crypto assets with AI-assisted review.",
    architecture: ["Holdings", "Market APIs", "P&L Engine", "Gemini Agent", "Dashboard"],
  },
};

function getProjectExtra(name) {
  return projectExtras[name] || {
    live: "",
    problem: "A focused AI product problem with a practical user workflow.",
    approach: "Python-first implementation using GenAI, data processing, and a deployable interface.",
    result: "A usable project designed around real interaction, not only a notebook demo.",
    architecture: ["Input", "Processing", "AI Layer", "API/UI", "Output"],
  };
}

function App() {
  const [profile, setProfile] = useState(fallbackProfile);
  const featuredCases = profile.projects.slice(0, 4);

  useEffect(() => {
    fetch(API_URL)
      .then((response) => (response.ok ? response.json() : Promise.reject()))
      .then(setProfile)
      .catch(() => setProfile(fallbackProfile));
  }, []);

  return (
    <main>
      <nav className="nav">
        <a href="#top" className="brand" aria-label="Arya Lolusare home">
          AL
        </a>
        <div className="nav-links">
          <a href="#projects">Projects</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
        </div>
      </nav>

      <header id="top" className="hero">
        <div className="hero-scene">
          <Suspense fallback={<div className="scene-fallback" aria-hidden="true" />}>
            <NeuralScene />
          </Suspense>
          <div className="project-radar" aria-label="Featured AI projects">
            <div className="radar-heading">
              <span>Featured AI builds</span>
              <strong>Project radar</strong>
            </div>
            <div className="radar-list">
              {profile.projects.slice(0, 3).map((project) => (
                <a href={project.repo} target="_blank" rel="noreferrer" key={project.name}>
                  <span>{project.name}</span>
                  <small>{project.stack.slice(0, 3).join(" / ")}</small>
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="hero-copy">
          <div className="status">
            <Sparkles size={16} />
            Building production-ready GenAI systems
          </div>
          <h1>{profile.name}</h1>
          <p className="role">{profile.title}</p>
          <p className="summary">{profile.summary}</p>
          <div className="hero-actions">
            <a className="button primary" href="#projects">
              View work <ArrowUpRight size={18} />
            </a>
            <a className="button" href={profile.github} target="_blank" rel="noreferrer">
              <Github size={18} /> GitHub
            </a>
          </div>
        </div>

        <aside className="hero-panel" aria-label="Profile snapshot">
          <img className="avatar" src={profile.avatar || fallbackProfile.avatar} alt={`${profile.name} GitHub avatar`} />
          <div>
            <h2>{profile.title}</h2>
            <p>
              <MapPin size={16} /> {profile.location}
            </p>
          </div>
          <div className="stat-grid">
            {profile.stats.map((stat) => (
              <div className="stat" key={stat.label}>
                <strong>{stat.value}</strong>
                <span>{stat.label}</span>
              </div>
            ))}
          </div>
        </aside>
      </header>

      <section className="signal-board" aria-label="AI systems focus">
        <div className="signal-copy">
          <BrainCircuit size={30} />
          <h2>AI systems that look good, but also do the hard work underneath.</h2>
          <p>
            The portfolio now presents you as a builder of usable GenAI products, not just demos: retrieval, agents,
            dashboards, APIs, and deployed workflows all get their own visual weight.
          </p>
        </div>
        <div className="signal-metrics">
          <div><strong>RAG</strong><span>contract risk scoring</span></div>
          <div><strong>4-agent</strong><span>problem solving flow</span></div>
          <div><strong>300+</strong><span>assets tracked in FinPilot</span></div>
          <div><strong>FastAPI</strong><span>backend-ready portfolio</span></div>
        </div>
      </section>

      <Section id="projects" eyebrow="Project Case Studies" title="From idea to architecture to live demo">
        <div className="case-grid">
          {featuredCases.map((project) => {
            const extra = getProjectExtra(project.name);
            return (
              <article className="case-card" key={`${project.name}-case`}>
                <div className="case-copy">
                  <Pill>{project.highlight}</Pill>
                  <h3>{project.name}</h3>
                  <dl>
                    <div>
                      <dt>Problem</dt>
                      <dd>{extra.problem}</dd>
                    </div>
                    <div>
                      <dt>Approach</dt>
                      <dd>{extra.approach}</dd>
                    </div>
                    <div>
                      <dt>Result</dt>
                      <dd>{extra.result}</dd>
                    </div>
                  </dl>
                  <div className="case-links">
                    {extra.live ? (
                      <a href={extra.live} target="_blank" rel="noreferrer">
                        Live demo <ArrowUpRight size={16} />
                      </a>
                    ) : null}
                    <a href={project.repo} target="_blank" rel="noreferrer">
                      Repository <Github size={16} />
                    </a>
                  </div>
                </div>
                <div className="architecture" aria-label={`${project.name} architecture`}>
                  {extra.architecture.map((step, index) => (
                    <div className="arch-node" key={step}>
                      <span>0{index + 1}</span>
                      <strong>{step}</strong>
                    </div>
                  ))}
                </div>
              </article>
            );
          })}
        </div>
      </Section>

      <section className="showcase">
        <div>
          <WandSparkles size={28} />
          <h2>From messy prompts to shipped AI workflows.</h2>
        </div>
        <p>
          I focus on retrieval quality, agent handoffs, model-grounded UX, and backend surfaces that make AI tools feel
          dependable in real use.
        </p>
      </section>

      <Section eyebrow="Build Method" title="A portfolio section that explains how you engineer AI systems">
        <div className="workflow-grid">
          {workflow.map((item) => {
            const Icon = item.icon || Sparkles;
            return (
              <article className="workflow-item" key={item.title}>
                <Icon size={24} />
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            );
          })}
        </div>
      </Section>

      <Section id="skills" eyebrow="Technical Range" title="LLM engineering, backend APIs, and data products">
        <div className="skill-summary">
          <article>
            <strong>01</strong>
            <span>Ground LLM outputs with retrieval and structured prompts.</span>
          </article>
          <article>
            <strong>02</strong>
            <span>Build agent flows that split research, coding, and critique.</span>
          </article>
          <article>
            <strong>03</strong>
            <span>Ship Python AI tools through APIs, dashboards, and demos.</span>
          </article>
        </div>
        <div className="skills">
          {Object.entries(profile.skills).map(([group, skills], groupIndex) => (
            <div className="skill-group" key={group}>
              <div className="skill-head">
                <div>
                  {(() => {
                    const Icon = skillMeta[group]?.icon || Sparkles;
                    return <Icon size={24} />;
                  })()}
                  <h3>{group}</h3>
                </div>
                <span>{String(groupIndex + 1).padStart(2, "0")}</span>
              </div>
              <p className="skill-focus">{skillMeta[group]?.focus}</p>
              <div className="skill-meter" style={{ "--level": `${skillMeta[group]?.level || 82}%` }} aria-hidden="true">
                <span />
              </div>
              <div className="skill-score">
                <span>Practical confidence</span>
                <strong>{skillMeta[group]?.level || 82}%</strong>
              </div>
              <div className="skill-tags">
                {skills.map((skill) => (
                  <Pill key={skill}>{skill}</Pill>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Section>

      <section className="split">
        <Section eyebrow="Education" title="Academic foundation">
          <div className="timeline">
            {profile.education.map((item) => (
              <article key={`${item.program}-${item.period}`}>
                <span>{item.period}</span>
                <h3>{item.program}</h3>
                <p>{item.school}</p>
                <small>{item.detail}</small>
              </article>
            ))}
          </div>
        </Section>

        <Section eyebrow="Certifications" title="Verified learning">
          <div className="certs">
            {profile.certifications.map((cert) => (
              <article key={cert.name}>
                <Trophy size={19} />
                <div>
                  <h3>{cert.name}</h3>
                  <p>
                    {cert.issuer} · {cert.date}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </Section>
      </section>

      <footer id="contact" className="contact">
        <div>
          <Terminal size={28} />
          <h2>Let’s build something intelligent.</h2>
          <p>Available for GenAI, RAG, multi-agent, and AI product collaborations.</p>
        </div>
        <div className="contact-links">
          <a href={`mailto:${profile.email}`}>
            <Mail size={18} /> {profile.email}
          </a>
          <a href={`tel:${profile.phone.replaceAll(" ", "")}`}>
            <Phone size={18} /> {profile.phone}
          </a>
          <a href={profile.github} target="_blank" rel="noreferrer">
            <Github size={18} /> GitHub
          </a>
          <a href={profile.linkedin} target="_blank" rel="noreferrer">
            <Linkedin size={18} /> LinkedIn
          </a>
        </div>
      </footer>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>,
);
