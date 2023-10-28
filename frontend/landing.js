import React from 'react';

function LandingPage() {
  return (
    <div>
      {/* Navbar */}
      <nav className="bg-blue-500 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <img src="/logo.png" alt="Hearts to Homes" className="h-8 w-8" />
            <a href="/" className="text-white">Home</a>
            <a href="/about" className="text-white">About</a>
            <a href="/homes" className="text-white">Homes</a>
          </div>
          <div>
            <a href="/login" className="text-white">Login</a>
            <a href="/register" className="bg-white text-blue-500 px-4 py-2 rounded-full">Register</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-hero-image bg-cover bg-center h-screen flex items-center text-white">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">Welcome to Hearts to Homes</h1>
          <p className="text-lg">Supporting Children's Homes Through Donations</p>
        </div>
      </div>

      {/* About Section */}
      <div className="bg-white p-8">
        <div className="container mx-auto flex items-center">
          <div className="w-1/2">
            <h2 className="text-2xl font-bold mb-4">About Us</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
          </div>
          <div className="w-1/2">
            <img src="/about-image.jpg" alt="About Hearts to Homes" className="w-full h-auto" />
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gray-100 py-8">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">Our Features</h2>
          <div className="flex flex-wrap justify-center">
            {/* Feature 1 */}
            <div className="w-full md:w-1/3 p-4">
              <div className="bg-feature-1 bg-cover bg-center h-32 text-white text-center p-4">
                <h3 className="text-xl font-bold mb-2">Feature 1</h3>
                <p>Some feature description here...</p>
              </div>
            </div>
            {/* Feature 2 */}
            <div className="w-full md:w-1/3 p-4">
              <div className="bg-feature-2 bg-cover bg-center h-32 text-white text-center p-4">
                <h3 className="text-xl font-bold mb-2">Feature 2</h3>
                <p>Another feature description here...</p>
              </div>
            </div>
            {/* Feature 3 */}
            <div className="w-full md:w-1/3 p-4">
              <div className="bg-feature-3 bg-cover bg-center h-32 text-white text-center p-4">
                <h3 className="text-xl font-bold mb-2">Feature 3</h3>
                <p>And one more feature description here...</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Donations Allocation Section */}
      <div className="container mx-auto flex py-8">
        <div className="w-1/2">
          <h2 className="text-3xl font-bold">Where Our Donations Go</h2>
          <p>40% - Home, 30% - Education, 20% - Healthcare, 10% - Other</p>
        </div>
        <div className="w-1/2">
          <img src="/piechart.png" alt="Donations Allocation" className="w-full h-auto" />
        </div>
      </div>

      {/* Events Section */}
      <div className="bg-gray-100 py-8">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">Upcoming Events</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Event 1 */}
            <div className="bg-white p-4 rounded shadow-md">
              <h3 className="text-xl font-bold">Event 1</h3>
              <p>Date: November 15, 2023</p>
              <p>Location: Event Venue</p>
            </div>
            {/* Event 2 */}
            <div className="bg-white p-4 rounded shadow-md">
              <h3 className="text-xl font-bold">Event 2</h3>
              <p>Date: November 20, 2023</p>
              <p>Location: Event Venue</p>
            </div>
            {/* Event 3 */}
            <div className="bg-white p-4 rounded shadow-md">
              <h3 className="text-xl font-bold">Event 3</h3>
              <p>Date: November 25, 2023</p>
              <p>Location: Event Venue</p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-500 text-white text-center py-4">
        <div className="container mx-auto">
          <p>&copy; 2023 Hearts to Homes</p>
          <p>"Changing Lives, One Heart at a Time."</p>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
