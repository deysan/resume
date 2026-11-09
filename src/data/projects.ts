import type { ImageMetadata } from "astro";
import mirrorCube from "../assets/projects/mirror-cube.webp";
import unicornReport from "../assets/projects/unicorn-report.png";

interface Project {
  id: string;
  name: string;
  subtitle?: string;
  category: string;
  description: string;
  detail: string;
  technologies: string[];
  testing?: string;
  note?: string;
  image: ImageMetadata;
  imageAlt: string;
  imageFocus?: "top";
  repository: string;
  demo: string;
  report?: { url: string; access: string };
}

export const projects: Project[] = [
  {
    id: "unicorn",
    name: "Unicorn",
    subtitle: "Quiz & Funnel Analytics",
    category: "Take-home project · Full-stack",
    description:
      "A three-step quiz and analytics dashboard with server-side offer selection, returning-user flows, and partner-confirmed leads and purchases.",
    detail:
      "Built with React and a Hono API on Cloudflare Workers, backed by D1/SQLite. Repeated partner callbacks are handled without double-counting results.",
    technologies: [
      "React",
      "TypeScript",
      "Hono",
      "Cloudflare Workers",
      "D1/SQLite",
      "Zod",
    ],
    testing: "Automated testing with Vitest and Playwright · GitHub Actions CI",
    note: "Public demo with synthetic data.",
    image: unicornReport,
    imageAlt:
      "Unicorn analytics report with date filters, quiz progression and funnel conversion metrics using synthetic data",
    imageFocus: "top",
    repository: "https://github.com/deysan/unicorn-funnel-analytics",
    demo: "https://unicorn-demo.unicorn-deysan.workers.dev/",
    report: {
      url: "https://unicorn-demo.unicorn-deysan.workers.dev/report",
      access: "Read-only access: demo / unicorn-demo",
    },
  },
  {
    id: "mirror-cube",
    name: "MirrorCube",
    category: "Personal project · Interactive 3D",
    description:
      "An interactive guide to solving a 2×2 Mirror Cube. Recreate a physical puzzle, find a solution, and follow animated steps in English or Ukrainian.",
    detail:
      "Built with React and Three.js, with solution search running in a Web Worker to keep the interface responsive.",
    technologies: [
      "React",
      "TypeScript",
      "Three.js",
      "React Three Fiber",
      "Web Workers",
    ],
    image: mirrorCube,
    imageAlt:
      "MirrorCube interface with a scrambled 3D puzzle and turn controls",
    repository: "https://github.com/deysan/mirror-cube",
    demo: "https://mirror-cube.netlify.app/",
  },
];
