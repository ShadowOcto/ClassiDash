const {ipcRenderer} = require("electron");
var DecompressZip = require('decompress-zip');
var fs = require('fs');
var exec = require('child_process').execFile;

var version = 0;
var updating = false;
var downloadDirectory = 'C:\\cdDevelopment\\NEW\\';

// If it doesn't have comments, ChatGPT didn't write it.

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function switchTab(tabName) {
    // Get all tab buttons and contents
    var tabButtons = document.querySelectorAll('.sidebar-top button');
    var tabContents = document.querySelectorAll('.tab-content');

    tabContents.forEach(function(tabContent) {
        tabContent.classList.remove('active');
    });

    tabButtons.forEach(function(tabButton) {
        tabButton.classList.remove('active');
    });

    // Show the selected tab content
    var selectedTabContent = document.getElementById(tabName + 'Tab');
    selectedTabContent.classList.add('active');

    // Activate the selected tab button
    var selectedTabButton = document.getElementById(tabName + 'Button');
    selectedTabButton.classList.add('active');
}

// Open the modal
function openModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
}

// Close the modal
function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

// Function to update progress bar
function updateProgress(progress) {
    var progressBar = document.getElementById('progressBar');
    progressBar.style.width = progress + '%';
}

function clearConsoleOutput() {
    var consoleOutput = document.getElementById('consoleOutput');
    consoleOutput.innerHTML = null;
}

// Function to update console output
function updateConsoleOutput(message) {
    var consoleOutput = document.getElementById('consoleOutput');
    consoleOutput.innerHTML += message + '<br>';
}

function updateProgress(progress) {
    var progressBar = document.getElementById('progressBar');
    progressBar.style.width = progress + '%';
}

function uncompress(ZIP_FILE_PATH, DESTINATION_PATH){
    var unzipper = new DecompressZip(ZIP_FILE_PATH);
    updateConsoleOutput('Extracting Update...')

    // Add the error event listener
    unzipper.on('error', function (err) {
        updateConsoleOutput(err)
    });
    
    // Notify when everything is extracted
    unzipper.on('extract', function (log) {
        updateConsoleOutput('Extracted Update.')
        fs.unlinkSync(DESTINATION_PATH + 'ClassiDash.zip');
        updateConsoleOutput('Cleaned up files.')
        updateConsoleOutput('Launching GDPS...')
        setTimeout(exec('ClassiDashNEW.exe', {cwd: DESTINATION_PATH +"\\ClassiDash\\"}), 2000)
        fs.writeFileSync(DESTINATION_PATH + 'version', version);
        updateConsoleOutput('Launched GDPS!')
        updating = false;
        sleep(2000).then(() => {closeModal(); });
    });
    
    // Notify "progress" of the decompressed files
    unzipper.on('progress', function (fileIndex, fileCount) {
        updateProgress(Math.floor(100 / (fileCount - (fileIndex + 1))))
    });
    
    // Unzip !
    unzipper.extract({
        path: DESTINATION_PATH
    });
}

async function handleDir() {
    if (!fs.existsSync('C:\\cdDevelopment\\')) {
        fs.mkdirSync('C:\\cdDevelopment\\');
    }

    if (fs.existsSync('C:\\cdDevelopment\\customInstallDir.txt')) {
        downloadDirectory = fs.readFileSync('C:\\cdDevelopment\\customInstallDir.txt').toString();
    } else {
        fs.writeFileSync('C:\\cdDevelopment\\customInstallDir.txt', 'C:\\cdDevelopment\\NEW\\');
    }

    if (!fs.existsSync(downloadDirectory)) {
        fs.mkdirSync(downloadDirectory);
    }
}

async function update() {
    openModal();

    if (updating) {
        updateConsoleOutput("Already updating...")
        return;
    }

    updating = true;

    const downloadUrl = 'https://classidash.fun/v2/download';
    var updateFound = false
    var localVersion = 0

    const updateCheckbox = document.getElementById('updateCheckbox');
    const checkForUpdates = updateCheckbox.checked;

    clearConsoleOutput();

    handleDir();
    if (fs.existsSync(downloadDirectory + 'ClassiDash.zip')) {
        fs.unlinkSync(downloadDirectory + 'ClassiDash.zip');
    }

    if (checkForUpdates) {
        updateConsoleOutput('Checking for updates...');
        const response = await fetch('https://classidash.fun/api/version');
        version = await response.text();

        if (fs.existsSync(downloadDirectory + 'version')) {
            localVersion = fs.readFileSync(downloadDirectory + 'version').toString();
            if (version > localVersion) updateFound = true;
        } else {
            fs.writeFileSync(downloadDirectory + 'version', '0');
            updateFound = true;
        }

        updateConsoleOutput('Server: ' + version + " Local: " + localVersion)
    }
    
    if (updateFound) {
        try {
            updateConsoleOutput('Selected download directory: ' + downloadDirectory);
            ipcRenderer.send("download", {
                url: downloadUrl,
                properties: {directory: downloadDirectory}
            });
                    updateConsoleOutput('Downloading Update...');
    
            ipcRenderer.on("download progress", (event, progress) => {
                const percentage = Math.floor(progress.percent * 100);
                updateProgress(percentage)
            });
    
            ipcRenderer.on("download complete", (event, file) => {
                updateConsoleOutput('Update Downloaded.')
                uncompress(downloadDirectory + 'ClassiDash.zip', downloadDirectory);
            });
    
        } catch (error) {
            updateConsoleOutput('Failed to download update :(');
            console.error('Error downloading update:', error);
            closeModal();
        }
    } else {
        exec('ClassiDashNEW.exe', {cwd: downloadDirectory +"\\ClassiDash\\"})
        updateConsoleOutput('Launched GDPS!')
        updating = false;
        sleep(2000).then(() => {closeModal(); });
    }
}

async function reinstall() {
    handleDir();
    fs.unlinkSync(downloadDirectory + 'version');
    update();
}

// Add an event listener to the launch button
document.getElementById('launchButton').addEventListener('click', update);

// Get the modal
var modal = document.getElementById('myModal');

// Get the close button
var span = document.getElementsByClassName('close')[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

closeModal();
switchTab('about');

// Function to fetch and display news stories
async function fetchAndDisplayNews() {
    try {
        const response = await fetch('https://classidash.fun/api/v2/news');
        const data = await response.json();

        const newsContainer = document.getElementById('newsContainer');

        newsContainer.innerHTML = '';

        const lastUpdated = document.createElement('p');
        lastUpdated.textContent = 'Last Updated: ' + data.lastUpdated;
        newsContainer.appendChild(lastUpdated);

        data.stories.forEach(story => {
            const storyElement = document.createElement('div');
            storyElement.classList.add('story');

            const title = document.createElement('h3');
            title.textContent = story.title;

            const description = document.createElement('p');
            description.textContent = story.desc;

            const image = document.createElement('img');
            image.src = story.img;
            
            storyElement.appendChild(image);
            storyElement.appendChild(title);
            storyElement.appendChild(description);

            newsContainer.appendChild(storyElement);
        });
    } catch (error) {
        const lastUpdated = document.createElement('p');
        lastUpdated.textContent = 'Failed to fetch news :('
        newsContainer.appendChild(lastUpdated);
        console.error('Error fetching news:', error);
    }
}

document.body.addEventListener('click', event => {
    if (event.target.tagName.toLowerCase() === 'a') {
      event.preventDefault();
      ipcRenderer.invoke('open-url', event.target.href)
    }
  });

window.addEventListener('load', fetchAndDisplayNews);
