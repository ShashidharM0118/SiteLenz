"""
Example: Using Groq API in SiteLenz

This file demonstrates how to integrate Groq API for various use cases
in the SiteLenz infrastructure monitoring system.
"""

from config_env import load_environment, get_api_key
from groq_helper import GroqClient


def analyze_defect(defect_type: str, image_description: str) -> str:
    """
    Get AI analysis of a detected defect.
    
    Args:
        defect_type: Type of defect detected (e.g., "major_crack")
        image_description: Description of what was captured
        
    Returns:
        Analysis and recommendations from AI
    """
    # Load environment and initialize client
    load_environment()
    api_key = get_api_key('GROQ_API_KEY')
    client = GroqClient(api_key, model=GroqClient.MODELS["mixtral"])
    
    # Create analysis prompt
    system_prompt = """You are a structural engineering assistant specializing in building defect analysis.
Provide concise, practical recommendations for detected defects."""
    
    message = f"""Analyze this building defect:
Type: {defect_type}
Description: {image_description}

Provide:
1. Severity assessment (Low/Medium/High)
2. Potential causes
3. Recommended actions
4. Urgency level

Keep response under 150 words."""
    
    # Get AI response
    response = client.chat(
        message=message,
        system_prompt=system_prompt,
        temperature=0.3  # Low temperature for consistent analysis
    )
    
    return response


def generate_inspection_summary(defects_list: list) -> str:
    """
    Generate a summary report of all detected defects.
    
    Args:
        defects_list: List of detected defects with details
        
    Returns:
        Formatted inspection summary
    """
    load_environment()
    api_key = get_api_key('GROQ_API_KEY')
    client = GroqClient(api_key, model=GroqClient.MODELS["llama3-8b"])
    
    # Format defects for the prompt
    defects_text = "\n".join([
        f"- {i+1}. {d['type']} (Confidence: {d['confidence']:.1%}) at {d['location']}"
        for i, d in enumerate(defects_list)
    ])
    
    message = f"""Generate an inspection summary for these detected defects:

{defects_text}

Include:
1. Overall assessment
2. Priority defects requiring immediate attention
3. General recommendations

Format as a professional inspection report. Keep under 200 words."""
    
    response = client.chat(
        message=message,
        system_prompt="You are a building inspector creating professional reports.",
        temperature=0.4
    )
    
    return response


def chat_with_voice_transcript(transcript: str, question: str) -> str:
    """
    Answer questions about voice transcript recordings.
    
    Args:
        transcript: Voice recording transcript
        question: User's question about the transcript
        
    Returns:
        AI response
    """
    load_environment()
    api_key = get_api_key('GROQ_API_KEY')
    client = GroqClient(api_key)
    
    message = f"""Based on this inspection voice transcript:
"{transcript}"

Question: {question}

Provide a clear, concise answer."""
    
    response = client.chat(
        message=message,
        system_prompt="You are an assistant helping with building inspection documentation.",
        temperature=0.5
    )
    
    return response


def streaming_analysis_example(defect_type: str):
    """
    Example of streaming response for real-time feedback.
    """
    load_environment()
    api_key = get_api_key('GROQ_API_KEY')
    client = GroqClient(api_key)
    
    print(f"\nStreaming analysis for {defect_type}:\n")
    print("AI: ", end="", flush=True)
    
    for chunk in client.chat_stream(
        message=f"Explain what causes {defect_type} in buildings and how to prevent it.",
        system_prompt="You are a structural engineering expert.",
        temperature=0.6
    ):
        print(chunk, end="", flush=True)
    
    print("\n")


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("SiteLenz - Groq API Integration Examples")
    print("=" * 70)
    
    # Example 1: Analyze a single defect
    print("\n1. Defect Analysis Example:")
    print("-" * 70)
    try:
        analysis = analyze_defect(
            defect_type="major_crack",
            image_description="Vertical crack in concrete wall, approximately 3mm wide, extending from floor to ceiling"
        )
        print(analysis)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Generate inspection summary
    print("\n2. Inspection Summary Example:")
    print("-" * 70)
    try:
        defects = [
            {"type": "major_crack", "confidence": 0.95, "location": "North wall"},
            {"type": "spalling", "confidence": 0.87, "location": "Column B-3"},
            {"type": "stain", "confidence": 0.76, "location": "Ceiling, Room 101"}
        ]
        summary = generate_inspection_summary(defects)
        print(summary)
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Chat with transcript
    print("\n3. Transcript Analysis Example:")
    print("-" * 70)
    try:
        transcript = "Found major crack on north wall, approximately 3mm wide. Water damage visible nearby. Recommend immediate attention."
        question = "What's the recommended action?"
        answer = chat_with_voice_transcript(transcript, question)
        print(f"Q: {question}")
        print(f"A: {answer}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Streaming response
    print("\n4. Streaming Response Example:")
    print("-" * 70)
    try:
        streaming_analysis_example("concrete spalling")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nIntegration tips:")
    print("- Use lower temperature (0.1-0.4) for technical analysis")
    print("- Use higher temperature (0.6-0.8) for creative content")
    print("- Use streaming for real-time user feedback")
    print("- Choose model based on speed vs capability needs")
    print("  - llama3-8b: Fastest, good for simple tasks")
    print("  - mixtral: Balanced, good for most use cases")
    print("  - llama3-70b: Most capable, slower but better analysis")
