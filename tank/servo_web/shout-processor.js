class ShoutProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.port.onmessage = event => {
      this.ws = event.data.ws;
    };
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (input && input[0]) {
      const buffer = input[0];
      const float32 = new Float32Array(buffer.length);
      for (let i = 0; i < buffer.length; i++) {
        float32[i] = buffer[i];
      }
      // 通过 port 发送回主线程，由主线程发送 WebSocket
      this.port.postMessage(float32.buffer, [float32.buffer]);
    }
    return true;
  }
}

registerProcessor('shout-processor', ShoutProcessor);
