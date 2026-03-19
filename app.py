import streamlit as st
import time
from config_manager import ConfigManager
from api_clients import APIClientFactory
from prompt_refiner import PromptRefiner
from theme_manager import ThemeManager


def init_session_state():
    """Initialize session state variables."""
    if 'config_manager' not in st.session_state:
        st.session_state.config_manager = ConfigManager()

    if 'refinement_result' not in st.session_state:
        st.session_state.refinement_result = ""

    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False

    if 'last_error' not in st.session_state:
        st.session_state.last_error = ""


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Rosetta Prompt",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    init_session_state()

    # Apply theme CSS (must be called early)
    ThemeManager.render_theme_selector()

    # App header
    st.title("Rosetta Prompt")
    st.markdown("""
    Transform clarifying questions and brain-dump answers into clear, well-structured responses.
    """)

    # Configuration sidebar
    config_manager = st.session_state.config_manager
    active_provider, config_valid = config_manager.render_config_ui()

    # Main interface
    st.header("Refinement Interface")

    # Create three columns for the main interface
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.subheader("Clarifying Questions")
        st.markdown("*The AI's original queries*")

        clarifying_questions = st.text_area(
            "AI Questions",
            placeholder="Example:\n1. What specific topic should the content focus on?\n2. Who is the target audience?\n3. What tone should be used?",
            height=300,
            key="clarifying_questions",
            label_visibility="collapsed"
        )

    with col2:
        st.subheader("Raw Responses")
        st.markdown("*Your unstructured draft answers*")

        raw_responses = st.text_area(
            "User Responses",
            placeholder="Example:\nI want to write about machine learning but for beginners. Make it friendly and approachable. I think it should cover basics like what ML is and maybe some simple examples.",
            height=300,
            key="raw_responses",
            label_visibility="collapsed"
        )

    with col3:
        st.subheader("Refined Output")
        st.markdown("*Structured answers ready to paste*")

        # Display the result or placeholder
        if st.session_state.refinement_result:
            st.text_area(
                "Refined Response",
                value=st.session_state.refinement_result,
                height=300,
                key="output_display",
                label_visibility="collapsed"
            )
        else:
            st.text_area(
                "Refined Response",
                placeholder="Your refined response will appear here after processing...",
                height=300,
                disabled=True,
                key="output_placeholder",
                label_visibility="collapsed"
            )

    # Control buttons
    st.markdown("---")

    # Create columns for buttons and status
    button_col1, button_col2, status_col = st.columns([1, 1, 2])

    with button_col1:
        # Main generate button
        generate_disabled = (
            not config_valid or
            not clarifying_questions.strip() or
            not raw_responses.strip() or
            st.session_state.is_processing
        )

        if st.button(
            "Refine",
            type="primary",
            disabled=generate_disabled,
            use_container_width=True,
            key="refine_response_button"
        ):
            if config_valid:
                process_refinement(active_provider, clarifying_questions, raw_responses)
            else:
                st.error("Please configure your LLM provider settings first.")

    with button_col2:
        # Clear button
        if st.button(
            "Clear All",
            disabled=st.session_state.is_processing,
            use_container_width=True,
            key="clear_all_button"
        ):
            st.session_state.refinement_result = ""
            st.session_state.last_error = ""
            st.rerun()

    with status_col:
        # Status display
        if st.session_state.is_processing:
            st.info("Processing your request...")
        elif st.session_state.last_error:
            st.error(st.session_state.last_error)
        elif st.session_state.refinement_result:
            st.success("Response refined successfully")

    # Input validation and tips
    st.markdown("---")

    with st.expander("Tips & Validation", expanded=False):
        # Validation status
        st.subheader("Input Validation")

        questions_valid = clarifying_questions.strip() and len(clarifying_questions.strip()) >= 10
        responses_valid = raw_responses.strip() and len(raw_responses.strip()) >= 10

        col_v1, col_v2 = st.columns(2)

        with col_v1:
            if questions_valid:
                st.success("Clarifying questions look good")
            else:
                st.warning("Please enter clarifying questions (min 10 characters)")

        with col_v2:
            if responses_valid:
                st.success("User responses look good")
            else:
                st.warning("Please enter user responses (min 10 characters)")

        # Tips
        st.subheader("Usage Tips")
        st.markdown("""
        **For Clarifying Questions:**
        - Copy the original questions from your AI conversation
        - Include all relevant questions, even if numbered or bulleted
        - Questions should be clear and specific

        **For Raw Responses:**
        - Include all your thoughts and requirements
        - Don't worry about formatting or structure
        - Be as detailed as possible about your needs

        **The Tool Will:**
        - Transform your brain-dump answers into clear, structured responses
        - Organize your thoughts to directly answer each question
        - Create natural responses you can paste back to the original AI
        """)

    # Copy functionality
    if st.session_state.refinement_result:
        st.markdown("---")
        with st.expander("Copy Refined Response", expanded=False):
            st.text_area(
                "Refined Response (Ready to Paste Back)",
                value=st.session_state.refinement_result,
                height=200,
                key="copy_refined_response",
                help="Copy this refined response and paste it back to the AI who asked the questions"
            )


def process_refinement(provider: str, questions: str, responses: str):
    """Process the prompt refinement request."""
    st.session_state.is_processing = True
    st.session_state.last_error = ""

    try:
        # Get provider configuration
        config_manager = st.session_state.config_manager
        provider_config = config_manager.get_provider_config(provider)

        # Validate inputs
        refiner = PromptRefiner(None)  # Temporary for validation
        is_valid, error_msg = refiner.validate_inputs(questions, responses)

        if not is_valid:
            st.session_state.last_error = error_msg
            return

        # Create LLM client
        llm_client = APIClientFactory.create_client(provider, provider_config)

        # Test connection first
        connection_ok, connection_msg = llm_client.test_connection()
        if not connection_ok:
            st.session_state.last_error = f"Connection test failed: {connection_msg}"
            return

        # Create refiner with the client
        refiner = PromptRefiner(llm_client)

        # Process the refinement
        with st.spinner(f"Refining prompt using {provider}..."):
            result = refiner.refine_prompt(questions, responses)
            st.session_state.refinement_result = result

    except ValueError as e:
        st.session_state.last_error = str(e)
    except Exception as e:
        st.session_state.last_error = f"Refinement failed: {str(e)}"

    finally:
        st.session_state.is_processing = False
        st.rerun()


if __name__ == "__main__":
    main()