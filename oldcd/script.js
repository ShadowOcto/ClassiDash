document.addEventListener('DOMContentLoaded', function() {
    // Get all tab links
    var tablinks = document.querySelectorAll('.tablink');

    // Get all tab contents
    var tabcontents = document.querySelectorAll('.tabcontent');

    // Loop through each tab link
    tablinks.forEach(function(tablink) {
        // Add click event listener
        tablink.addEventListener('click', function(event) {
            // Prevent default behavior
            event.preventDefault();

            // Remove 'active' class from all tab links
            tablinks.forEach(function(tl) {
                tl.classList.remove('active');
            });

            // Add 'active' class to clicked tab link
            tablink.classList.add('active');

            // Hide all tab contents
            tabcontents.forEach(function(tc) {
                tc.style.display = 'none';
            });

            // Show the corresponding tab content
            var targetId = tablink.getAttribute('data-target');
            document.getElementById(targetId).style.display = 'block';
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Array of subtitle options
    var subtitles = [
        "The BEST 2.1 GDPS", // ClassiDash Trailer
        "classidash.fun", // ClassiDash Domain
        "Untamed Is Top 1", // Untamed is NOT top 1
        "Free Demon", // Free Demon
        "Wave Carried", // Everyone is wave carried
        "2 Attempts (lost some due to crashes)", // SacrificeGD
        "DISCRETION IS ADVISED", // DISCRETION ADVISED
        "FIREWORK'S DEMISE", // DISCRETION ADVISED Description
        "Better Than CP6", // True
        "#CP6FEETDEEP",
        "Rule 11", // No Yapping Allowed
        "NEW BEST! 94%", // Hykre Untamed 94%
        "Can I Have BURN?", // He really wants it
        "BABY GIRL YOU BREAK MY HEART", // i dont wna cry
        "Wet In", // Dry Out
        "#hall-of-shame", // Check the channel
        "IT DIDN'T CLIP!", // R.I.P Hykre
        "FUN!, Enjoy!, Thanks For Playing!", // Faithful by Shadow
        "50K GOLD CHAIN", // no chance
        "Cry About It", // 100k views
        "BOUND TO FALLING IN LOVVEEEEE", // Bound / Denis Video
        "Show Me Your Love", // Fantasy
        "BURNING LIKE A CANDLE LIGHT", // BURN
        "Why Do You Have No Mats?", // Ash Moment
        "FluffyGorilla21", // Hykre Moment
        "Every Single ClassiDash MEMBER Has My Face", // Lodomir Moment
        "September 25th, 2022, 7:47PM, United Kingdom", // Shadow Moment
        "Enter The Farhan", // FARLUSION
        "Enter The Seb", // SEBLUSION
        "IF YOU'RE INSECURE, JUST SAY IT DAWG", // Denis NC Quote
        "THE ORB I HIT THE ORB" // Hexeract Geometry Dash
    ];

    // Get the subtitle element
    var subtitleElement = document.querySelector("#home .subtitle");

    // Pick a random subtitle from the array
    var randomIndex = Math.floor(Math.random() * subtitles.length);
    var randomSubtitle = subtitles[randomIndex];

    // Set the random subtitle as the text content of the subtitle element
    subtitleElement.textContent = randomSubtitle;
});