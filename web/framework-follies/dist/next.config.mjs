import createNextJsObfuscator from "nextjs-obfuscator";

const withNextJsObfuscator = createNextJsObfuscator(
  {
    deadCodeInjection: true,
    debugProtection: true,
    disableConsoleOutput: true,
    selfDefending: true,
  },
  {},
);

const nextConfig = withNextJsObfuscator({
  output: "standalone",
  productionBrowserSourceMaps: false,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
});
// const nextConfig = {
//   productionBrowserSourceMaps: false,
//   eslint: {
//     ignoreDuringBuilds: true,
//   },
//   typescript: {
//     ignoreBuildErrors: true,
//   },
// };

export default nextConfig;
