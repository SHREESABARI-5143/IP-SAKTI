/** @type {import('next').NextConfig} */
const nextConfig = {
  devIndicators: false,
  typescript: {
    // Pure JS project — ignore Next.js internal TS checks
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
