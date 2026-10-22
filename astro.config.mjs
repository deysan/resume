import { defineConfig } from "astro/config";

export default defineConfig({
  output: "static",
  site: "https://deysan.github.io",
  base: "/resume/",
  trailingSlash: "always",
  build: {
    inlineStylesheets: "always",
  },
});
