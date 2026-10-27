import mirrorCube from "../assets/projects/mirror-cube.webp";

export const projects = [
  {
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
