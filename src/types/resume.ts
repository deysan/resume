import type resume from "../data/resume.json";

export type Resume = typeof resume;
export type Experience = Resume["experience"][number];
export type Course =
  Resume["learning"][number] | Resume["moreLearning"][number];
