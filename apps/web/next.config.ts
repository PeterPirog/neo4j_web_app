import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@neo4j-web-app/api-client"],
};

export default nextConfig;
