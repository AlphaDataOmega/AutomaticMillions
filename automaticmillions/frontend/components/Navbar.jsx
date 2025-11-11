// Top navigation bar scaffold.

export default function Navbar() {
  // TODO: Populate navigation with links and responsive behavior.
  return (
    <header className="w-full flex items-center justify-between px-4 py-3 bg-white shadow">
      <span className="text-lg font-semibold">AutomaticMillions</span>
      <nav className="space-x-4 text-sm text-gray-600">
        <a href="#features">Features</a>
        <a href="#pricing">Pricing</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
}
