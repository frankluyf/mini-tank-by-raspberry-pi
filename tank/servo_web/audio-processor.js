/**
 * 这个处理器运行在独立的音频线程中。
 * 它的任务是接收音频输入，并通过 postMessage 将数据发送回主线程。
 */
class AudioRecorderProcessor extends AudioWorkletProcessor {
  // process 方法是核心，每次音频缓冲区准备好时都会被调用
  process(inputs, outputs, parameters) {
    // inputs[0] 代表第一个输入源（我们的麦克风）
    // inputs[0][0] 代表该输入源的第一个声道（我们是单声道）
    const audioData = inputs[0][0];

    // 如果没有音频数据（例如，麦克风被静音），则什么也不做
    if (!audioData) {
      return true; // 返回 true 以保持处理器活动
    }

    // 将 Float32Array 格式的音频数据发送回主线程
    // 我们传递 audioData.buffer 来转移所有权，这比复制更高效
    this.port.postMessage(audioData, [audioData.buffer]);

    // 必须返回 true，否则处理器会自动停止
    return true;
  }
}

// 注册这个处理器，给它起一个名字 'audio-recorder-processor'
// 主线程将通过这个名字来创建它的实例
registerProcessor('audio-recorder-processor', AudioRecorderProcessor);