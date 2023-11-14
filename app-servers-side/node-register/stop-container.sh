if nvidia-smi; then
    echo "Found GPU on the Node, starting the GPU services..."
    exec bash node-gpu/stop-gpu.sh
else
    echo "No GPU found on the node, starting the CPU services..."
    exec bash node-cpu/stop-cpu.sh
fi
