import streamlit as st
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    page_title="Speech App",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #667eea;
        font-size: 3rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    .description {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .tts-container {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 2px dashed #dcdcdc;
    }

    .tts-header {
        text-align: center;
        color: #4a4a4a;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎤 Speech to Text App</h1>', unsafe_allow_html=True)
st.markdown('<p class="description">Click "Start" to begin converting your speech to text in real-time</p>', unsafe_allow_html=True)

# Create columns for better layout for STT
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Embed the HTML/JavaScript speech-to-text interface
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: transparent;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            
            .container {
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                width: 100%;
                max-width: 500px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            #transcript {
                background: #f8f9fa;
                color: #333;
                border: 2px solid #e9ecef;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                min-height: 120px;
                font-size: 1.1em;
                line-height: 1.6;
                white-space: pre-wrap;
                overflow-y: auto;
                max-height: 200px;
            }
            
            .buttons {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 20px;
            }
            
            button {
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                min-width: 80px;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            #startBtn {
                background: linear-gradient(45deg, #2ecc71, #27ae60);
                color: white;
            }
            
            #startBtn:hover {
                background: linear-gradient(45deg, #27ae60, #2ecc71);
            }
            
            #stopBtn {
                background: linear-gradient(45deg, #e74c3c, #c0392b);
                color: white;
            }
            
            #stopBtn:hover {
                background: linear-gradient(45deg, #c0392b, #e74c3c);
            }
            
            .status {
                text-align: center;
                margin-top: 15px;
                font-size: 0.9em;
                color: #666;
                min-height: 20px;
            }
            
            .listening {
                color: #2ecc71 !important;
                font-weight: bold;
            }
            
            .error {
                color: #e74c3c;
                background: #ffeaea;
                padding: 10px;
                border-radius: 8px;
                margin-top: 10px;
                text-align: center;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="transcript">Click "Start" and speak clearly into your microphone...</div>
            <div class="buttons">
                <button id="startBtn">🎤 Start</button>
                <button id="stopBtn">⏹️ Stop</button>
            </div>
            <div id="status" class="status">Ready to listen</div>
            <div id="error" class="error" style="display: none;"></div>
        </div>

        <script>
            let recognition = null;
            let isListening = false;
            let finalTranscript = '';
            
            const transcript = document.getElementById('transcript');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            const status = document.getElementById('status');
            const errorDiv = document.getElementById('error');

            // Check for speech recognition support
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';

                recognition.onstart = () => {
                    isListening = true;
                    status.textContent = 'Listening... Speak now!';
                    status.classList.add('listening');
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    errorDiv.style.display = 'none';
                };

                recognition.onend = () => {
                    isListening = false;
                    status.textContent = 'Ready to listen';
                    status.classList.remove('listening');
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                };

                recognition.onresult = (e) => {
                    let interimTranscript = '';
                    
                    for (let i = e.resultIndex; i < e.results.length; i++) {
                        const transcriptPart = e.results[i][0].transcript;
                        
                        if (e.results[i].isFinal) {
                            finalTranscript += transcriptPart + ' ';
                        } else {
                            interimTranscript += transcriptPart;
                        }
                    }
                    
                    transcript.textContent = finalTranscript + interimTranscript;
                    transcript.scrollTop = transcript.scrollHeight;
                };

                recognition.onerror = (event) => {
                    let errorMsg = 'Error: ';
                    switch(event.error) {
                        case 'no-speech':
                            errorMsg += 'No speech detected. Please try again.';
                            break;
                        case 'audio-capture':
                            errorMsg += 'No microphone found.';
                            break;
                        case 'not-allowed':
                            errorMsg += 'Microphone access denied.';
                            break;
                        default:
                            errorMsg += event.error;
                    }
                    errorDiv.textContent = errorMsg;
                    errorDiv.style.display = 'block';
                };

                startBtn.onclick = () => {
                    if (recognition && !isListening) {
                        recognition.start();
                    }
                };

                stopBtn.onclick = () => {
                    if (recognition && isListening) {
                        recognition.stop();
                    }
                };

                // Initialize button states
                stopBtn.disabled = true;
                
            } else {
                errorDiv.textContent = 'Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.';
                errorDiv.style.display = 'block';
                startBtn.disabled = true;
                stopBtn.disabled = true;
            }
        </script>
    </body>
    </html>
    """
    
    # Display the HTML component
    components.html(html_code, height=400, scrolling=False)

# --------------------------------------------------
# New Text to Speech Section
# --------------------------------------------------
st.markdown('<div class="tts-container"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="tts-header">🔊 Text to AI Speech</h2>', unsafe_allow_html=True)
st.markdown('<p class="description">Enter text below and click "Speak" to hear it read aloud.</p>', unsafe_allow_html=True)

tts_text = st.text_area("Enter text here:", height=150, key="tts_input")

if st.button("Speak"):
    if tts_text:
        # Use an HTML component to handle the TTS functionality in the browser
        # Note: The Web Speech API is used here as a standard way to achieve this.
        # It leverages the user's browser for speech synthesis, which is the most
        # common implementation for a simple Streamlit app without external APIs.
        tts_html_code = f"""
        <!DOCTYPE html>
        <html>
        <body>
        <script>
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance("{tts_text.replace('"', '\\"')}");
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert('Text-to-speech not supported in this browser.');
            }}
        </script>
        </body>
        </html>
        """
        components.html(tts_html_code, height=0)
    else:
        st.warning("Please enter some text to speak.")


# Add some information in the sidebar
with st.sidebar:
    st.markdown("### ℹ️ Information")
    st.markdown("""
    **How to use (Speech to Text):**
    1. Click the "Start" button
    2. Allow microphone access when prompted
    3. Speak clearly into your microphone
    4. Click "Stop" when finished
    
    **How to use (Text to AI Speech):**
    1. Enter text into the text box
    2. Click the "Speak" button
    3. Ensure your volume is up to hear the output

    **Requirements:**
    - Modern browser (Chrome, Edge, Safari)
    - Microphone access permission (for STT)
    - Internet connection
    
    **Features:**
    - Real-time speech recognition
    - Text-to-speech playback
    """)
    
    st.markdown("### 🔧 Technical Details")
    st.markdown("""
    This app uses the **Web Speech API** built into modern browsers. 
    The speech recognition happens entirely in your browser - 
    no audio data is sent to external servers.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    Built with Streamlit | Speech recognition powered by Web Speech API
</div>
""", unsafe_allow_html=True)
