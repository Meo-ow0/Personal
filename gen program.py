<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generative AI Site Builder</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f7f9;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .mode-button {
            transition: all 0.2s;
        }
        .mode-button.active {
            background-color: #4f46e5;
            color: white;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
        }
        /* Style for displaying the generated content */
        .output-card {
            min-height: 200px;
        }
        #text-output {
            white-space: pre-wrap; /* Preserves formatting and line breaks from the AI */
        }
        .image-placeholder {
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px dashed #a0aec0;
            color: #4a5568;
            font-style: italic;
        }
    </style>
</head>
<body class="p-4 md:p-8">

    <!-- Container for the Application -->
    <div class="container">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-2">
            AI Creation Hub
        </h1>
        <p class="text-lg text-gray-500 mb-8">
            Build your own multi-functional generative site. Select a mode below to begin.
        </p>

        <!-- Mode Selection Buttons -->
        <div class="flex space-x-4 mb-8">
            <button id="mode-text" onclick="setMode('text')"
                class="mode-button px-6 py-2 rounded-xl bg-white text-gray-700 font-semibold border border-gray-300 active">
                ✍️ Text Generator
            </button>
            <button id="mode-image" onclick="setMode('image')"
                class="mode-button px-6 py-2 rounded-xl bg-white text-gray-700 font-semibold border border-gray-300">
                🖼️ Image Generator
            </button>
        </div>

        <!-- Input Section -->
        <div class="bg-white p-6 rounded-2xl shadow-xl">
            <h2 id="input-title" class="text-2xl font-bold mb-4 text-indigo-600">
                Text Generation Mode
            </h2>
            <textarea id="user-prompt"
                class="w-full p-4 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 transition duration-150"
                rows="4" placeholder="Enter your prompt here... (e.g., Write a 500-word story about a robot who loves classical music)"></textarea>

            <button id="generate-button" onclick="handleGeneration()"
                class="mt-4 w-full md:w-auto px-8 py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition duration-150">
                Generate Content
            </button>
        </div>

        <!-- Output Section -->
        <div class="mt-8 p-6 rounded-2xl shadow-xl bg-white output-card">
            <h2 class="text-2xl font-bold mb-4 border-b pb-2 text-gray-800">
                Generated Output
            </h2>
            <div id="loading-indicator" class="hidden text-center py-10">
                <div class="animate-spin inline-block w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
                <p class="mt-2 text-indigo-600 font-semibold">Generating...</p>
            </div>
            <div id="output-display">
                <div id="text-output" class="text-gray-700 leading-relaxed">
                    <!-- Text generation output will appear here -->
                </div>
                <div id="image-output" class="hidden grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- Image generation output will appear here -->
                </div>
                <div id="initial-message" class="image-placeholder">
                    Your generated content will appear here.
                </div>
            </div>
        </div>

        <p id="error-message" class="text-red-500 mt-4 font-semibold hidden">
            An error occurred. Please try again.
        </p>
    </div>

    <script>
        // Global variables provided by the Canvas environment for the API key.
        const apiKey = ""; 

        let currentMode = 'text';

        // Helper function for exponential backoff during API calls
        async function fetchWithRetry(url, options, maxRetries = 3) {
            for (let attempt = 0; attempt < maxRetries; attempt++) {
                try {
                    const response = await fetch(url, options);
                    if (!response.ok) {
                         // Throw error for non-2xx responses
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response;
                } catch (error) {
                    console.error(`Attempt ${attempt + 1} failed:`, error);
                    if (attempt === maxRetries - 1) {
                        throw error;
                    }
                    const delay = Math.pow(2, attempt) * 1000;
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        /**
         * Switches the application between Text and Image generation modes.
         */
        function setMode(mode) {
            currentMode = mode;
            document.getElementById('mode-text').classList.remove('active');
            document.getElementById('mode-image').classList.remove('active');

            const title = document.getElementById('input-title');
            const promptArea = document.getElementById('user-prompt');
            const button = document.getElementById('generate-button');

            if (mode === 'text') {
                document.getElementById('mode-text').classList.add('active');
                title.textContent = "Text Generation Mode";
                promptArea.placeholder = "Enter your prompt here... (e.g., Write a short article on quantum computing)";
                button.textContent = "Generate Text";
                document.getElementById('text-output').classList.remove('hidden');
                document.getElementById('image-output').classList.add('hidden');
            } else {
                document.getElementById('mode-image').classList.add('active');
                title.textContent = "Image Generation Mode";
                promptArea.placeholder = "Enter a detailed prompt for your image... (e.g., A photorealistic golden retriever wearing a tiny astronaut helmet, cinematic lighting)";
                button.textContent = "Generate Image";
                document.getElementById('text-output').classList.add('hidden');
                document.getElementById('image-output').classList.remove('hidden');
            }
            // Clear outputs on mode change
            document.getElementById('text-output').innerHTML = '';
            document.getElementById('image-output').innerHTML = '';
            document.getElementById('initial-message').classList.remove('hidden');
            document.getElementById('error-message').classList.add('hidden');
        }

        /**
         * Main handler to start the generation process based on the current mode.
         */
        async function handleGeneration() {
            const prompt = document.getElementById('user-prompt').value.trim();
            if (!prompt) {
                alert("Please enter a prompt.");
                return;
            }

            document.getElementById('error-message').classList.add('hidden');
            document.getElementById('initial-message').classList.add('hidden');
            document.getElementById('loading-indicator').classList.remove('hidden');
            
            // Clear previous outputs
            document.getElementById('text-output').innerHTML = '';
            document.getElementById('image-output').innerHTML = '';

            try {
                if (currentMode === 'text') {
                    await generateText(prompt);
                } else {
                    await generateImage(prompt);
                }
            } catch (error) {
                console.error("Generation failed:", error);
                document.getElementById('error-message').textContent = `Generation failed: ${error.message || 'An API error occurred.'}`;
                document.getElementById('error-message').classList.remove('hidden');
            } finally {
                document.getElementById('loading-indicator').classList.add('hidden');
            }
        }

        /**
         * LLM Service Call 1: Text Generation (using gemini-2.5-flash-preview-05-20)
         */
        async function generateText(prompt) {
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

            const payload = {
                contents: [{ parts: [{ text: prompt }] }],
                // Add Google Search grounding for fresh knowledge, like the guide suggests
                tools: [{ "google_search": {} }], 
            };

            const response = await fetchWithRetry(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            const text = result?.candidates?.[0]?.content?.parts?.[0]?.text;

            if (text) {
                document.getElementById('text-output').textContent = text;
            } else {
                document.getElementById('text-output').textContent = "Could not generate text. Model might have blocked the content.";
            }
        }

        /**
         * LLM Service Call 2: Image Generation (using imagen-3.0-generate-002)
         */
        async function generateImage(prompt) {
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key=${apiKey}`;

            // Image generation models often require specific parameters
            const payload = {
                instances: [{ prompt: prompt }],
                parameters: {
                    sampleCount: 2, // Generate 2 images
                    aspectRatio: "1:1",
                    outputMimeType: "image/png"
                }
            };

            const response = await fetchWithRetry(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            const images = result?.predictions;
            const imageOutputDiv = document.getElementById('image-output');
            
            if (images && images.length > 0) {
                imageOutputDiv.innerHTML = ''; // Clear output

                images.forEach((prediction, index) => {
                    if (prediction.bytesBase64Encoded) {
                        const imageUrl = `data:image/png;base64,${prediction.bytesBase64Encoded}`;
                        
                        const imgWrapper = document.createElement('div');
                        imgWrapper.className = 'bg-gray-100 rounded-lg overflow-hidden shadow-lg';
                        
                        const img = document.createElement('img');
                        img.src = imageUrl;
                        img.alt = `Generated Image ${index + 1}`;
                        img.className = 'w-full h-auto object-cover rounded-t-lg';
                        
                        // Simple Download button
                        const downloadLink = document.createElement('a');
                        downloadLink.href = imageUrl;
                        downloadLink.download = `ai_image_${index + 1}.png`;
                        downloadLink.textContent = 'Download';
                        downloadLink.className = 'block text-center py-2 bg-indigo-500 text-white hover:bg-indigo-600 rounded-b-lg font-medium';
                        
                        imgWrapper.appendChild(img);
                        imgWrapper.appendChild(downloadLink);
                        imageOutputDiv.appendChild(imgWrapper);
                    }
                });
            } else {
                imageOutputDiv.innerHTML = '<p class="text-gray-500">No images were generated. The prompt may have been unsafe or invalid.</p>';
            }
        }

        // Initialize mode when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            setMode('text');
        });
    </script>
</body>
</html>