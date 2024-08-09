document.addEventListener("DOMContentLoaded", function() {
    // Get references to the buttons
    const contactUsBtn = document.getElementById("contactUsBtn");
    const hoursBtn = document.getElementById("hoursBtn");
    const aboutUsBtn = document.getElementById("aboutUsBtn");

    // Add event listeners to the buttons
    contactUsBtn.addEventListener("click", function() {
        // Functionality to display contact us content
        displayContactUsContent();
    });

    hoursBtn.addEventListener("click", function() {
        // Functionality to display hours content
        displayHoursContent();
    });

    aboutUsBtn.addEventListener("click", function() {
        // Functionality to display about us content
        displayAboutUsContent();
    });

    displayHoursContent();
});

function displayContactUsContent() {
    // Update the content container with contact us content
    const contentContainer = document.getElementById("contentContainer");
    contentContainer.innerHTML = "<h2>Contact Us</h2><p>Send us an email at mom@familyasianmarket.com or call us at (904) 513-3151</p>";
}

function displayHoursContent() {
    // Update the content container with hours content
    const contentContainer = document.getElementById("contentContainer");
    contentContainer.innerHTML = "<h2>Hours</h2><p>Sunday: 10:00 am to 7:00 pm</p><p>Monday: 10:00 am to 7:00 pm</p><p>Tuesday: 10:00 am to 7:00 pm</p><p>Wednesday: Closed</p><p>Thursday: 10:00 am to 7:00 pm</p><p>Friday: 10:00 am to 7:00 pm</p><p>Saturday: 10:00 am to 7:00 pm</p>";
}

function displayAboutUsContent() {
    // Update the content container with about us content
    const contentContainer = document.getElementById("contentContainer");
    contentContainer.innerHTML = "<h2>About Us</h2><p>Our family immigrated to the United States in 2012. After 9 years, we founded Family Asian Market.  We are a full-service Asian Grocery Store that has become an important part of the local community. Come down and meet us.</p>";
}
