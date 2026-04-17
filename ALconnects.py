#!/usr/bin/env python3
"""
Arya Lolusare - Portfolio Website
Run: python portfolio.py
Then open: http://localhost:8080
"""

import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8080

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Arya Lolusare — AI/ML Engineer</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Space+Mono:ital,wght@0,400;1,400&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0a0a0a;
    --surface: #111111;
    --surface2: #181818;
    --border: rgba(255,255,255,0.07);
    --border-hover: rgba(255,255,255,0.14);
    --text: #f0ede8;
    --muted: #888580;
    --accent: #c8f055;
    --accent2: #55f0c8;
    --accent3: #f05580;
    --font-head: 'Space Grotesk', sans-serif;
    --font-serif: 'DM Serif Display', serif;
    --font-mono: 'Space Mono', monospace;
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-head);
    overflow-x: hidden;
    cursor: none;
  }

  /* Custom cursor */
  #cursor {
    width: 12px; height: 12px;
    background: var(--accent);
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    transform: translate(-50%, -50%);
    transition: transform 0.1s, width 0.2s, height 0.2s, background 0.2s;
    mix-blend-mode: difference;
  }
  #cursor-ring {
    width: 36px; height: 36px;
    border: 1px solid rgba(200,240,85,0.4);
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 9998;
    transform: translate(-50%, -50%);
    transition: transform 0.15s ease-out, width 0.2s, height 0.2s;
  }

  /* Noise overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
  }

  /* Nav */
  nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 3rem;
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(20px);
    background: rgba(10,10,10,0.7);
  }

  .nav-logo {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: var(--text);
    text-decoration: none;
  }
  .nav-logo span { color: var(--accent); }

  .nav-links { display: flex; gap: 2rem; list-style: none; }
  .nav-links a {
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s;
  }
  .nav-links a:hover { color: var(--accent); }

  /* Hero */
  #hero {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    padding: 6rem 3rem 4rem;
    position: relative;
    overflow: hidden;
    gap: 2rem;
  }

  .hero-left {
    display: flex;
    flex-direction: column;
    z-index: 1;
  }

  .hero-right {
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
    position: relative;
    height: 480px;
  }

  /* Orb */
  .orb-container {
    position: relative;
    width: 420px;
    height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .orb-core {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #e8ff80, #c8f055 40%, #6abf00 80%, #2a4d00);
    box-shadow:
      0 0 40px rgba(200,240,85,0.6),
      0 0 80px rgba(200,240,85,0.3),
      0 0 140px rgba(200,240,85,0.15);
    animation: orbPulse 3s ease-in-out infinite;
    position: relative;
    z-index: 5;
  }

  @keyframes orbPulse {
    0%, 100% { box-shadow: 0 0 40px rgba(200,240,85,0.6), 0 0 80px rgba(200,240,85,0.3), 0 0 140px rgba(200,240,85,0.15); transform: scale(1); }
    50% { box-shadow: 0 0 60px rgba(200,240,85,0.8), 0 0 110px rgba(200,240,85,0.45), 0 0 180px rgba(200,240,85,0.2); transform: scale(1.06); }
  }

  .orbit-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(200,240,85,0.15);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
  }

  .orbit-ring-1 { width: 200px; height: 200px; border-color: rgba(200,240,85,0.2); animation: spinOrbit 8s linear infinite; }
  .orbit-ring-2 { width: 290px; height: 290px; border-color: rgba(200,240,85,0.12); animation: spinOrbit 14s linear infinite reverse; }
  .orbit-ring-3 { width: 380px; height: 380px; border-color: rgba(200,240,85,0.07); animation: spinOrbit 20s linear infinite; }

  @keyframes spinOrbit { from { transform: translate(-50%, -50%) rotate(0deg); } to { transform: translate(-50%, -50%) rotate(360deg); } }

  .orbit-dot {
    position: absolute;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px rgba(200,240,85,0.8);
  }

  /* Tech pills on orbits */
  .orbit-pill {
    position: absolute;
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    color: var(--accent);
    background: rgba(200,240,85,0.08);
    border: 1px solid rgba(200,240,85,0.25);
    padding: 0.25rem 0.6rem;
    border-radius: 2px;
    white-space: nowrap;
    pointer-events: none;
  }

  /* Ring 1 pills */
  .r1-pill-1 { top: -10px; left: 50%; transform: translateX(-50%); }
  .r1-pill-2 { bottom: -10px; left: 50%; transform: translateX(-50%); }

  /* Ring 2 pills */
  .r2-pill-1 { top: -12px; left: 50%; transform: translateX(-50%); }
  .r2-pill-2 { bottom: -12px; left: 50%; transform: translateX(-50%); }
  .r2-pill-3 { left: -28px; top: 50%; transform: translateY(-50%); }

  /* Ring 3 pills */
  .r3-pill-1 { top: -12px; left: 50%; transform: translateX(-50%); }
  .r3-pill-2 { bottom: -12px; left: 50%; transform: translateX(-50%); }
  .r3-pill-3 { right: -36px; top: 50%; transform: translateY(-50%); }
  .r3-pill-4 { left: -28px; top: 50%; transform: translateY(-50%); }

  .hero-bg-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: clamp(120px, 18vw, 280px);
    font-weight: 800;
    letter-spacing: -0.04em;
    color: rgba(255,255,255,0.02);
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
    z-index: 0;
  }

  .hero-tag {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeUp 0.6s 0.2s forwards;
  }

  .hero-name {
    font-size: clamp(3rem, 9vw, 8rem);
    font-weight: 800;
    line-height: 0.92;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeUp 0.7s 0.4s forwards;
  }

  .hero-name em {
    font-family: var(--font-serif);
    font-style: italic;
    font-weight: 400;
    color: var(--accent);
  }

  .hero-desc {
    font-size: clamp(1rem, 1.6vw, 1.25rem);
    color: var(--muted);
    max-width: 520px;
    line-height: 1.6;
    font-weight: 400;
    margin-bottom: 2.5rem;
    opacity: 0;
    animation: fadeUp 0.7s 0.6s forwards;
  }

  .hero-cta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.7s 0.8s forwards;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.75rem;
    font-family: var(--font-head);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-decoration: none;
    border-radius: 2px;
    transition: all 0.2s;
    cursor: none;
  }
  .btn-primary {
    background: var(--accent);
    color: #0a0a0a;
    border: 1px solid var(--accent);
  }
  .btn-primary:hover { background: transparent; color: var(--accent); }
  .btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border-hover);
  }
  .btn-outline:hover { border-color: var(--accent); color: var(--accent); }

  .scroll-indicator {
    position: absolute;
    bottom: 2rem;
    right: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    opacity: 0;
    animation: fadeIn 1s 1.5s forwards;
  }
  .scroll-indicator span {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    writing-mode: vertical-rl;
  }
  .scroll-line {
    width: 1px;
    height: 60px;
    background: linear-gradient(to bottom, var(--accent), transparent);
    animation: scrollPulse 2s 2s infinite;
  }

  /* Sections */
  section {
    padding: 7rem 3rem;
    position: relative;
    z-index: 1;
  }

  .section-label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1rem;
  }

  .section-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.05;
    margin-bottom: 3rem;
  }

  /* About */
  #about { background: var(--surface); }

  .about-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5rem;
    align-items: start;
  }

  .about-text p {
    font-size: 1.1rem;
    line-height: 1.8;
    color: var(--muted);
    margin-bottom: 1.5rem;
    font-weight: 400;
  }
  .about-text p strong { color: var(--text); font-weight: 700; }

  .about-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-top: 2rem;
  }
  .stat {
    background: var(--surface);
    padding: 1.5rem;
  }
  .stat-num {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 0.25rem;
  }
  .stat-label {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: var(--muted);
    text-transform: uppercase;
  }

  .skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 2rem;
  }
  .skill-tag {
    padding: 0.4rem 0.9rem;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    border: 1px solid var(--border-hover);
    color: var(--muted);
    transition: all 0.2s;
    letter-spacing: 0.05em;
  }
  .skill-tag:hover { border-color: var(--accent); color: var(--accent); background: rgba(200,240,85,0.05); }
  .skill-tag.highlight { border-color: var(--accent); color: var(--accent); background: rgba(200,240,85,0.08); }

  /* Projects */
  #projects { background: var(--bg); }

  .projects-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
  }

  .project-card {
    background: var(--bg);
    padding: 2.5rem;
    position: relative;
    overflow: hidden;
    transition: background 0.3s;
    text-decoration: none;
    display: block;
    color: inherit;
    cursor: none;
  }

  .project-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 0;
    background: var(--accent);
    transition: height 0.3s;
  }
  .project-card:hover::before { height: 100%; }
  .project-card:hover { background: var(--surface2); }

  .project-num {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    margin-bottom: 1.25rem;
  }

  .project-title {
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
    transition: color 0.2s;
  }
  .project-card:hover .project-title { color: var(--accent); }

  .project-desc {
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--muted);
    margin-bottom: 1.5rem;
    font-weight: 400;
  }

  .project-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }
  .tech-pill {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    padding: 0.25rem 0.6rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--muted);
    letter-spacing: 0.05em;
  }

  .project-arrow {
    position: absolute;
    top: 2.5rem;
    right: 2.5rem;
    font-size: 1.2rem;
    color: var(--border-hover);
    transition: all 0.3s;
  }
  .project-card:hover .project-arrow { color: var(--accent); transform: translate(4px, -4px); }

  /* GitHub repos */
  .repos-list {
    margin-top: 2rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .repo-card {
    border: 1px solid var(--border);
    padding: 1.25rem 1.5rem;
    text-decoration: none;
    color: inherit;
    display: block;
    transition: all 0.2s;
    cursor: none;
    background: var(--surface);
  }
  .repo-card:hover { border-color: var(--accent2); background: var(--surface2); }
  .repo-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--accent2);
    margin-bottom: 0.4rem;
  }
  .repo-desc {
    font-size: 0.75rem;
    color: var(--muted);
    line-height: 1.5;
    font-weight: 400;
  }
  .repo-lang {
    margin-top: 0.75rem;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .lang-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3572A5;
    display: inline-block;
  }

  /* Education */
  #education { background: var(--surface); }

  .edu-timeline {
    position: relative;
    padding-left: 2rem;
  }
  .edu-timeline::before {
    content: '';
    position: absolute;
    left: 0; top: 0.5rem; bottom: 0;
    width: 1px;
    background: var(--border);
  }

  .edu-item {
    position: relative;
    padding-bottom: 2.5rem;
    opacity: 0;
    transform: translateX(-20px);
    transition: all 0.5s;
  }
  .edu-item.visible { opacity: 1; transform: none; }

  .edu-item::before {
    content: '';
    position: absolute;
    left: -2rem;
    top: 0.5rem;
    width: 9px; height: 9px;
    border-radius: 50%;
    background: var(--accent);
    transform: translateX(-4px);
    box-shadow: 0 0 0 3px rgba(200,240,85,0.15);
  }

  .edu-year {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--accent);
    letter-spacing: 0.15em;
    margin-bottom: 0.4rem;
  }
  .edu-degree { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.2rem; }
  .edu-school { font-size: 0.9rem; color: var(--muted); }

  /* Contact */
  #contact { background: var(--bg); text-align: center; }

  .contact-inner { max-width: 640px; margin: 0 auto; }

  .contact-big {
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 1.5rem;
  }
  .contact-big em {
    font-family: var(--font-serif);
    font-style: italic;
    font-weight: 400;
    color: var(--accent);
  }

  .contact-sub {
    font-size: 1rem;
    color: var(--muted);
    margin-bottom: 3rem;
    font-weight: 400;
    line-height: 1.6;
  }

  .contact-links {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
  }

  .contact-link {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.75rem 1.5rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-decoration: none;
    border: 1px solid var(--border-hover);
    color: var(--muted);
    transition: all 0.2s;
    cursor: none;
  }
  .contact-link:hover { color: var(--accent); border-color: var(--accent); background: rgba(200,240,85,0.05); }

  /* Footer */
  footer {
    border-top: 1px solid var(--border);
    padding: 2rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.08em;
  }

  /* Animations */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  @keyframes scrollPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
  }

  /* Responsive */
  @media (max-width: 768px) {
    nav { padding: 1rem 1.5rem; }
    section { padding: 5rem 1.5rem; }
    #hero { grid-template-columns: 1fr; padding: 7rem 1.5rem 4rem; }
    .hero-right { height: 300px; }
    .orb-container { width: 280px; height: 280px; }
    .orbit-ring-3 { width: 260px; height: 260px; }
    .orbit-ring-2 { width: 200px; height: 200px; }
    .orbit-ring-1 { width: 140px; height: 140px; }
    .orb-core { width: 80px; height: 80px; }
    .about-grid { grid-template-columns: 1fr; gap: 2.5rem; }
    .projects-grid { grid-template-columns: 1fr; }
    .repos-list { grid-template-columns: 1fr; }
    footer { flex-direction: column; gap: 0.75rem; text-align: center; }
    .nav-links { display: none; }
  }
</style>
</head>
<body>

<div id="cursor"></div>
<div id="cursor-ring"></div>

<!-- NAV -->
<nav>
  <a href="#hero" class="nav-logo">AL<span>.</span></a>
  <ul class="nav-links">
    <li><a href="#about">About</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#education">Education</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hero-bg-text">AI/ML</div>

  <!-- Left column -->
  <div class="hero-left">
    <div class="hero-tag">AI / ML Engineer · Nagpur, India</div>

    <h1 class="hero-name">
      Arya<br/>
      <em>Lolusare</em>
    </h1>

    <p class="hero-desc">
      AI/ML Engineering student building real-world intelligent systems —
      LLMs, RAG pipelines, multi-agent architectures, and generative AI tools.
    </p>

    <div class="hero-cta">
      <a href="#projects" class="btn btn-primary">View Projects &darr;</a>
      <a href="https://github.com/AryaLolusare2712" target="_blank" class="btn btn-outline">GitHub &rarr;</a>
      <a href="https://www.linkedin.com/in/arya-lolusare-6530662b4/" target="_blank" class="btn btn-outline">LinkedIn &rarr;</a>
      <a href="mailto:aryalolusare0909@gmail.com" class="btn btn-outline">Email Me</a>
    </div>
  </div>

  <!-- Right column — Glowing orb with orbiting tech rings -->
  <div class="hero-right">
    <div class="orb-container">

      <!-- Ring 1 -->
      <div class="orbit-ring orbit-ring-1">
        <span class="orbit-pill r1-pill-1">Python</span>
        <span class="orbit-pill r1-pill-2">PyTorch</span>
      </div>

      <!-- Ring 2 -->
      <div class="orbit-ring orbit-ring-2">
        <span class="orbit-pill r2-pill-1">LangChain</span>
        <span class="orbit-pill r2-pill-2">RAG</span>
        <span class="orbit-pill r2-pill-3">Gradio</span>
      </div>

      <!-- Ring 3 -->
      <div class="orbit-ring orbit-ring-3">
        <span class="orbit-pill r3-pill-1">Multi-Agent</span>
        <span class="orbit-pill r3-pill-2">Streamlit</span>
        <span class="orbit-pill r3-pill-3">Vector DB</span>
        <span class="orbit-pill r3-pill-4">LLMs</span>
      </div>

      <!-- Core orb -->
      <div class="orb-core"></div>
    </div>
  </div>

  <div class="scroll-indicator">
    <div class="scroll-line"></div>
    <span>Scroll</span>
  </div>
</section>

<!-- ABOUT -->
<section id="about">
  <div class="section-label">// 01 — About</div>
  <h2 class="section-title">Building the<br/>intelligent future</h2>

  <div class="about-grid">
    <div class="about-text">
      <p>
        I'm a <strong>B.Tech Information Technology</strong> student at G.H. Raisoni College of Engineering, Nagpur, graduating in 2027. My passion lies at the intersection of <strong>language models, autonomous agents, and real-world AI applications</strong>.
      </p>
      <p>
        I work with Python, PyTorch, LangChain, and Gradio to build systems that actually solve problems — from meeting synthesizers to multi-agent problem solvers. Every project is an experiment in making AI more useful, accessible, and intelligent.
      </p>

      <div class="about-stats">
        <div class="stat">
          <div class="stat-num">16+</div>
          <div class="stat-label">GitHub Repos</div>
        </div>
        <div class="stat">
          <div class="stat-num">4+</div>
          <div class="stat-label">AI Projects</div>
        </div>
        <div class="stat">
          <div class="stat-num">2027</div>
          <div class="stat-label">Graduating</div>
        </div>
        <div class="stat">
          <div class="stat-num">∞</div>
          <div class="stat-label">Curiosity</div>
        </div>
      </div>
    </div>

    <div>
      <div class="section-label" style="margin-bottom:1.25rem;">Tech Stack</div>
      <div class="skills-grid">
        <span class="skill-tag highlight">Python</span>
        <span class="skill-tag highlight">LLMs</span>
        <span class="skill-tag highlight">LangChain</span>
        <span class="skill-tag highlight">RAG</span>
        <span class="skill-tag highlight">Multi-Agent Systems</span>
        <span class="skill-tag">PyTorch</span>
        <span class="skill-tag">Transformers</span>
        <span class="skill-tag">Scikit-learn</span>
        <span class="skill-tag">Gradio</span>
        <span class="skill-tag">Vector Embeddings</span>
        <span class="skill-tag">NLP</span>
        <span class="skill-tag">Deep Learning</span>
        <span class="skill-tag">REST APIs</span>
        <span class="skill-tag">MySQL</span>
        <span class="skill-tag">Git</span>
        <span class="skill-tag">Java</span>
        <span class="skill-tag">Streamlit</span>
        <span class="skill-tag">Jupyter</span>
      </div>
    </div>
  </div>
</section>

<!-- PROJECTS -->
<section id="projects">
  <div class="section-label">// 02 — Projects</div>
  <h2 class="section-title">Things I've<br/>built</h2>

  <div class="projects-grid">

    <a class="project-card" href="https://github.com/AryaLolusare2712/Multi-Agent-Problem-Solver" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">01 &mdash; Featured</div>
      <div class="project-title">Multi-Agent Problem Solver</div>
      <p class="project-desc">
        A collaborative AI system where specialized agents analyze problems, generate solutions, and produce structured reports. Powered by RAG with vector embeddings for contextual understanding.
      </p>
      <div class="project-tech">
        <span class="tech-pill">Python</span>
        <span class="tech-pill">LangChain</span>
        <span class="tech-pill">RAG</span>
        <span class="tech-pill">Vector Embeddings</span>
        <span class="tech-pill">Gradio</span>
      </div>
    </a>

    <a class="project-card" href="https://github.com/AryaLolusare2712/SiteCraft" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">02 &mdash; GenAI</div>
      <div class="project-title">SiteCraft &mdash; AI Website Generator</div>
      <p class="project-desc">
        Generate production-ready codebases (frontend, backend, DB) from prompts, templates, or design preferences. Crafting websites with AI magic.
      </p>
      <div class="project-tech">
        <span class="tech-pill">Python</span>
        <span class="tech-pill">LLMs</span>
        <span class="tech-pill">Jupyter</span>
        <span class="tech-pill">Code Gen</span>
      </div>
    </a>

    <a class="project-card" href="https://github.com/AryaLolusare2712/DataLens" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">03 &mdash; Data</div>
      <div class="project-title">DataLens &mdash; AI Analytics Dashboard</div>
      <p class="project-desc">
        AI-powered data analytics dashboard built with Streamlit. Upload CSV/Excel files to instantly explore data, visualize trends, and chat with your dataset using LLMs.
      </p>
      <div class="project-tech">
        <span class="tech-pill">Python</span>
        <span class="tech-pill">Streamlit</span>
        <span class="tech-pill">Pandas</span>
        <span class="tech-pill">LLMs</span>
        <span class="tech-pill">Scikit-learn</span>
      </div>
    </a>

    <a class="project-card" href="https://github.com/AryaLolusare2712/DigestAI" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">04 &mdash; Research</div>
      <div class="project-title">DigestAI &mdash; Research Paper Digestion</div>
      <p class="project-desc">
        AI-powered tool that processes research papers and converts complex academic content into digestible summaries and structured insights.
      </p>
      <div class="project-tech">
        <span class="tech-pill">Python</span>
        <span class="tech-pill">NLP</span>
        <span class="tech-pill">LLMs</span>
        <span class="tech-pill">Summarization</span>
      </div>
    </a>

    <a class="project-card" href="https://github.com/AryaLolusare2712" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">05 &mdash; NLP</div>
      <div class="project-title">Smart Meeting Synthesizer</div>
      <p class="project-desc">
        AI-powered meeting assistant that processes transcripts and automatically generates summaries and key action points using LLM-based text summarization.
      </p>
      <div class="project-tech">
        <span class="tech-pill">Python</span>
        <span class="tech-pill">NLP</span>
        <span class="tech-pill">LLMs</span>
        <span class="tech-pill">Gradio</span>
      </div>
    </a>

    <a class="project-card" href="https://github.com/AryaLolusare2712/CodeLabs" target="_blank">
      <div class="project-arrow">&#x2197;</div>
      <div class="project-num">06 &mdash; Platform</div>
      <div class="project-title">CodeLabs &mdash; Collaborative Coding</div>
      <p class="project-desc">
        Real-time collaborative coding platform enabling multiple developers to write, review, and iterate on code simultaneously in a shared environment.
      </p>
      <div class="project-tech">
        <span class="tech-pill">HTML</span>
        <span class="tech-pill">JavaScript</span>
        <span class="tech-pill">Real-time</span>
        <span class="tech-pill">WebSockets</span>
      </div>
    </a>

  </div>

  <!-- More GitHub repos -->
  <div class="section-label" style="margin-top:4rem; margin-bottom:1.5rem;">// More on GitHub</div>
  <div class="repos-list">
    <a class="repo-card" href="https://github.com/AryaLolusare2712/Dataset_Generator_using_LLM" target="_blank">
      <div class="repo-name">Dataset Generator using LLM</div>
      <div class="repo-desc">Generate synthetic datasets using large language models for ML training.</div>
      <div class="repo-lang"><span class="lang-dot"></span> Python</div>
    </a>
    <a class="repo-card" href="https://github.com/AryaLolusare2712" target="_blank">
      <div class="repo-name">AI Healthcare Assistant</div>
      <div class="repo-desc">Veterinary chatbot for pet & livestock health guidance using NLP + LLMs.</div>
      <div class="repo-lang"><span class="lang-dot"></span> Python</div>
    </a>
    <a class="repo-card" href="https://github.com/AryaLolusare2712/ALconnects" target="_blank">
      <div class="repo-name">ALconnects — Portfolio Site</div>
      <div class="repo-desc">Personal developer portfolio built with Python & vanilla HTML/CSS — the site you're looking at right now.</div>
      <div class="repo-lang"><span class="lang-dot"></span> Python</div>
    </a>
  </div>
</section>

<!-- EDUCATION -->
<section id="education">
  <div class="section-label">// 03 — Education</div>
  <h2 class="section-title">Academic<br/>journey</h2>

  <div class="edu-timeline">
    <div class="edu-item">
      <div class="edu-year">2023 &mdash; 2027 (Expected)</div>
      <div class="edu-degree">B.Tech — Information Technology</div>
      <div class="edu-school">G.H. Raisoni College of Engineering, Nagpur</div>
    </div>
    <div class="edu-item">
      <div class="edu-year">2021 &mdash; 2023</div>
      <div class="edu-degree">Higher Secondary (XII)</div>
      <div class="edu-school">Prerna Jr. College, Nagpur</div>
    </div>
    <div class="edu-item">
      <div class="edu-year">Until 2021</div>
      <div class="edu-degree">Secondary Schooling (X)</div>
      <div class="edu-school">Jain International School, Nagpur</div>
    </div>
  </div>
</section>

<!-- CONTACT -->
<section id="contact">
  <div class="contact-inner">
    <div class="section-label" style="margin-bottom:1.5rem;">// 04 — Contact</div>
    <div class="contact-big">
      Let's<br/><em>connect</em>
    </div>
    <p class="contact-sub">
      I'm always open to interesting AI/ML projects, collaborations,
      internships, or just a great conversation about LLMs.
    </p>
    <div class="contact-links">
      <a class="contact-link" href="mailto:aryalolusare0909@gmail.com">
        ✉ Email
      </a>
      <a class="contact-link" href="https://github.com/AryaLolusare2712" target="_blank">
        &#x2665; GitHub
      </a>
      <a class="contact-link" href="tel:+918830280151">
        &#x260E; +91 88302 80151
      </a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <span>Arya Lolusare &mdash; Nagpur, India</span>
  <span>Built with Python &bull; 2025</span>
  <span>AI/ML Engineer</span>
</footer>

<script>
  // Custom cursor
  const cursor = document.getElementById('cursor');
  const ring = document.getElementById('cursor-ring');
  let mx = 0, my = 0, rx = 0, ry = 0;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx + 'px';
    cursor.style.top = my + 'px';
  });

  function animRing() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.left = rx + 'px';
    ring.style.top = ry + 'px';
    requestAnimationFrame(animRing);
  }
  animRing();

  document.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.style.width = '20px';
      cursor.style.height = '20px';
      ring.style.width = '56px';
      ring.style.height = '56px';
    });
    el.addEventListener('mouseleave', () => {
      cursor.style.width = '12px';
      cursor.style.height = '12px';
      ring.style.width = '36px';
      ring.style.height = '36px';
    });
  });

  // Scroll reveal for education items
  const observer = new IntersectionObserver(entries => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 150);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.edu-item').forEach(el => observer.observe(el));

  // Active nav link
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 100) current = s.id;
    });
    navLinks.forEach(a => {
      a.style.color = a.getAttribute('href') === '#' + current
        ? 'var(--accent)'
        : 'var(--muted)';
    });
  });
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def log_message(self, format, *args):
        pass  # Suppress request logs for clean output


def open_browser():
    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    print(f"\n  🚀  Arya Lolusare — Portfolio")
    print(f"  ──────────────────────────────")
    print(f"  Server running at: http://localhost:{PORT}")
    print(f"  Opening browser automatically...")
    print(f"  Press Ctrl+C to stop.\n")

    threading.Thread(target=open_browser, daemon=True).start()

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped. Goodbye! 👋\n")
