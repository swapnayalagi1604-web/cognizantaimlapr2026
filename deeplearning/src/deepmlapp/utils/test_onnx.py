import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("loan_approval_pipeline.onnx")

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

input_data = np.array(
    [[76710, 452, 23]],
    dtype=np.float32
)

output = session.run(
    [output_name],
    {input_name: input_data}
)

score = output[0][0][0]

print("Score:", score)
print("Prediction:", "Loan Approved" if score > 0.5 else "Loan Rejected")