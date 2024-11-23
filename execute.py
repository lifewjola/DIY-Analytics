import io
import sys

def execute_generated_code(code, df):
    clean_code = code.strip('```').strip()  # Clean the code by removing block markers and spaces
    
    # Redirect stdout to capture print statements
    output_buffer = io.StringIO()
    sys.stdout = output_buffer  # Set the custom stdout to capture printed output
    
    # Pass the DataFrame to the local scope
    local_scope = {"df": df}
    
    try:
        # Execute the code with the DataFrame in the local scope
        exec(clean_code, {}, local_scope)
    except Exception as e:
        return f"Error during execution: {e}"
    finally:
        # Reset stdout to default after execution
        sys.stdout = sys.__stdout__
    
    # Return both the output captured and the local scope (for plots or other variables)
    output = output_buffer.getvalue()
    return local_scope, output
