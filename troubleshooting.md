# Ollama on OpenShift Troubleshooting

## Common Issues and Solutions

### GPU Not Detected

If Ollama is not detecting your GPU:

1. Check that the GPU operator is properly installed:
   ```bash
   oc get pods -n nvidia-gpu-operator
   ```

2. Verify GPU resources are available:
   ```bash
   oc describe node <node-name> | grep -A 10 Capacity
   ```

3. Ensure your Deployment requests GPU resources:
   ```yaml
   resources:
     limits:
       nvidia.com/gpu: 1
   ```

### High Memory Usage

Mistral and other large models require significant memory. If you're experiencing OOM (Out of Memory) errors:

1. Increase the memory limit in your Deployment
2. Use a more memory-efficient quantized model (e.g., Q4_0 instead of Q8_0)
3. Consider using a smaller model if hardware constraints are tight

### Slow Model Loading

Model loading can be slow initially. Solutions:

1. Pre-download models during container startup
2. Use persistent storage (PVC) to avoid redownloading models after pod restarts

### API Connection Issues

If clients can't connect to the API:

1. Verify route is created correctly:
   ```bash
   oc get route ollama -n ollama
   ```

2. Check network policy allows traffic:
   ```bash
   oc get networkpolicy -n ollama
   ```

3. Test connection directly from inside the cluster:
   ```bash
   oc exec -it deploy/ollama -n ollama -- curl localhost:11434/api/tags
   ```
