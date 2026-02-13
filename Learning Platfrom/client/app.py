import streamlit as st
import requests

# Configuration
API_URL = "http://localhost:8001"

st.set_page_config(page_title="EduCore", layout="wide")

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("client/static/style.css")
except FileNotFoundError:
    st.warning("CSS file not found. Ensure client/static/style.css exists.")


# Session State Initialization
if 'roadmap' not in st.session_state:
    st.session_state['roadmap'] = None
if 'content_cache' not in st.session_state:
    st.session_state['content_cache'] = {}
if 'current_chapter_index' not in st.session_state:
    st.session_state['current_chapter_index'] = None

st.title("EduCore: AI Learning Platform")

# Sidebar - Course Generation
with st.sidebar:
    st.header("Create Course")
    topic = st.text_input("Topic", "Quantum Physics")
    grade = st.selectbox("Grade Level", ["Grade 8", "Grade 10", "Undergraduate", "PhD"])
    
    if st.button("Generate Roadmap"):
        with st.spinner("Consulting AI Agents..."):
            try:
                payload = {"topic": topic, "grade_level": grade}
                response = requests.post(f"{API_URL}/generate/course", json=payload)
                response.raise_for_status()
                data = response.json()
                st.session_state['roadmap'] = data['roadmap']
                st.session_state['content_cache'] = {} # Reset cache
                st.session_state['current_chapter_index'] = None
                st.success("Roadmap Generated!")
            except Exception as e:
                st.error(f"Error: {e}")

    st.divider()
    st.header("Proctoring Status")
    st.info("Camera inactive (Streamlit Dumb Terminal). In production, this would stream to WS.")

# Main Usage - Master-Detail View
if st.session_state['roadmap']:
    roadmap = st.session_state['roadmap']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(f"Roadmap: {roadmap['topic']}")
        st.caption("Select a chapter to learn")
        
        for idx, chapter in enumerate(roadmap['chapters']):
            # Button for each chapter
            if st.button(f"Chapter {chapter['chapter_number']}: {chapter['title']}", key=f"btn_{idx}", use_container_width=True):
                st.session_state['current_chapter_index'] = idx

    with col2:
        idx = st.session_state['current_chapter_index']
        if idx is not None:
            chapter = roadmap['chapters'][idx]
            
            # Check Cache
            if idx in st.session_state['content_cache']:
                content = st.session_state['content_cache'][idx]
            else:
                with st.spinner(f"Generating comprehensive content for: {chapter['title']}..."):
                    try:
                        payload = {
                            "chapter": chapter,
                            "topic": roadmap['topic'],
                            "grade_level": grade # Note: technically grade might have changed in sidebar, but acceptable for MVP
                        }
                        response = requests.post(f"{API_URL}/generate/chapter", json=payload)
                        response.raise_for_status()
                        content = response.json()
                        st.session_state['content_cache'][idx] = content
                    except Exception as e:
                        st.error(f"Failed to generate content: {e}")
                        content = None

            if content:
                st.header(content['chapter_title'])
                st.markdown(content['content_markdown'])
                
                # --- Video Generation ---
                st.divider()
                st.subheader("Video Summary 🎥")
                
                video_key = f"video_{idx}"
                if video_key not in st.session_state:
                    st.session_state[video_key] = None
                    
                if st.session_state[video_key]:
                    # Display existing video
                    video_url = f"{API_URL}{st.session_state[video_key]}"
                    st.video(video_url)
                else:
                    if st.button("Generate Video Summary", key=f"gen_vid_{idx}"):
                        with st.spinner("Generating video (this may take a minute)..."):
                            try:
                                vid_payload = {
                                    "topic": content['chapter_title'],
                                    "content_markdown": content['content_markdown']
                                }
                                vid_resp = requests.post(f"{API_URL}/generate/video", json=vid_payload)
                                vid_resp.raise_for_status()
                                vid_data = vid_resp.json()
                                st.session_state[video_key] = vid_data['video_url']
                                st.rerun()
                            except Exception as e:
                                st.error(f"Video generation failed: {e}")

                st.divider()
                st.subheader("Knowledge Check")
                
                # Unique key for this chapter's quiz state
                quiz_key = f"quiz_started_{idx}"
                
                if quiz_key not in st.session_state:
                    st.session_state[quiz_key] = False

                if not st.session_state[quiz_key]:
                    if st.button("Start Quiz 📝", key=f"start_{idx}"):
                        st.session_state[quiz_key] = True
                        st.rerun()
                else:
                    with st.form(key=f"quiz_form_{idx}"):
                        user_answers = {}
                        for i, q in enumerate(content['quiz']):
                            st.write(f"**Q{i+1}: {q['question']}**")
                            # Radio button for options
                            user_detail = st.radio(
                                "Select Answer:", 
                                q['options'], 
                                key=f"q_{idx}_{i}", 
                                index=None, # No default selection
                                label_visibility="collapsed"
                            )
                            user_answers[i] = user_detail

                        submitted = st.form_submit_button("Submit Answers 🚀")
                        
                        if submitted:
                            score = 0
                            total = len(content['quiz'])
                            
                            for i, q in enumerate(content['quiz']):
                                selected = user_answers.get(i)
                                correct_opt = q['options'][q['correct_answer']]
                                
                                if selected == correct_opt:
                                    score += 1
                                    st.success(f"Q{i+1}: Correct! ✅")
                                else:
                                    st.error(f"Q{i+1}: Incorrect ❌. The right answer was: {correct_opt}")
                            
                            final_score = (score / total) * 100
                            st.metric(label="Your Score", value=f"{final_score:.0f}%", delta=f"{score}/{total} Correct")
                            
                            if score == total:
                                st.balloons()
                            elif score >= total / 2:
                                st.snow()
        else:
            st.info("👈 Select a chapter from the timeline to begin.")

else:
    st.info("Enter a topic on the left to start your learning journey.")
