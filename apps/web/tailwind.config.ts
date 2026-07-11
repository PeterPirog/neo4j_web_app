import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/features/**/*.{ts,tsx}",
    "./src/lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        graph: {
          ink: "#17201b",
          line: "#d7ded8",
          surface: "#f7f8f6",
          accent: "#246b57",
          warn: "#b45309",
        },
      },
    },
  },
  plugins: [],
};

export default config;
