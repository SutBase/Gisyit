// -*- coding: utf-8 -*-
/**
 * React版本的视频解析组件
 */

import React, { useState } from 'react';
import { parseVideoUrl } from '../../api/api';
import { useDownloadHistory } from '../../composables/useDownloadHistory';

const VideoParser = ({ onVideoParsed }) => {
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoResult, setVideoResult] = useState(null);
  const [error, setError] = useState('');
  const { addToHistory } = useDownloadHistory();

  // 解析视频
  const parseVideo = async () => {
    const url = videoUrl.trim();
    if (!url) {
      setError('请输入视频链接');
      return;
    }

    setLoading(true);
    setError('');
    setVideoResult(null);

    try {
      const result = await parseVideoUrl(url);
      setVideoResult(result);
      onVideoParsed(result);
    } catch (err) {
      setError(err.message || '解析视频时发生错误');
    } finally {
      setLoading(false);
    }
  };

  // 下载视频
  const downloadVideo = (stream, video) => {
    // 添加到下载历史
    addToHistory({
      title: video.title,
      platform: video.platform,
      quality: stream.quality,
      format: stream.format,
      timestamp: new Date().toISOString()
    });

    // 触发下载
    const link = document.createElement('a');
    link.href = stream.url;
    link.download = `${video.title}_${stream.quality}.${stream.format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // 格式化时长
  const formatDuration = (seconds) => {
    if (!seconds || seconds <= 0) return '未知';

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
      return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
  };

  return (
    <div className="video-parser">
      <div className="card">
        <div className="card-body">
          <div className="mb-4">
            <label htmlFor="videoUrl" className="form-label">视频链接</label>
            <div className="input-group">
              <input 
                type="text" 
                className="form-control" 
                id="videoUrl" 
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                placeholder="粘贴视频链接..."
                onKeyUp={(e) => e.key === 'Enter' && parseVideo()}
              />
              <button className="btn btn-primary" type="button" onClick={parseVideo} disabled={loading}>
                {!loading ? (
                  <>
                    <i className="bi bi-search"></i> 解析
                  </>
                ) : (
                  <>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    解析中...
                  </>
                )}
              </button>
            </div>
            <div className="form-text">支持哔哩哔哩、抖音、YouTube等主流视频平台</div>
          </div>

          {loading && (
            <div className="loading">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">解析中...</span>
              </div>
              <p className="mt-2">正在解析视频，请稍候...</p>
            </div>
          )}

          {videoResult && (
            <div className="video-result">
              <div className="card">
                <div className="card-header">
                  <h5 className="card-title mb-0">
                    <span className="platform-badge">{videoResult.platform}</span>
                    {videoResult.title}
                  </h5>
                </div>
                <div className="card-body">
                  {videoResult.cover ? (
                    <div className="row">
                      <div className="col-md-4">
                        <img src={videoResult.cover} className="img-fluid rounded" alt="视频封面" />
                      </div>
                      <div className="col-md-8">
                        <p><strong>时长:</strong> {formatDuration(videoResult.duration)}</p>
                      </div>
                    </div>
                  ) : (
                    <p><strong>时长:</strong> {formatDuration(videoResult.duration)}</p>
                  )}

                  {videoResult.downloadable && videoResult.streams && videoResult.streams.length > 0 ? (
                    <>
                      <h6>可用下载选项:</h6>
                      <div className="streams-container">
                        {videoResult.streams.map((stream, index) => (
                          <div key={index} className="stream-item">
                            <div className="d-flex justify-content-between align-items-center">
                              <div>
                                <span className="badge bg-primary">{stream.quality}</span>
                                <span className="badge bg-secondary">{stream.format}</span>
                                {stream.has_watermark ? (
                                  <span className="badge bg-warning">含水印</span>
                                ) : (
                                  <span className="badge bg-success">无水印</span>
                                )}
                              </div>
                              <a 
                                href={stream.url} 
                                className="btn btn-sm btn-success" 
                                onClick={(e) => {
                                  e.preventDefault();
                                  downloadVideo(stream, videoResult);
                                }}
                              >
                                <i className="bi bi-download"></i> 下载
                              </a>
                            </div>
                        ))}
                      </div>
                    </>
                  ) : (
                    <div className="alert alert-warning">
                      <i className="bi bi-exclamation-triangle-fill"></i> {videoResult.reason || '此视频无法下载'}
                    </div>
                  )}
                </div>
              </div>

              {videoResult.disclaimer && (
                <div className="alert alert-info alert-disclaimer mt-3">
                  <i className="bi bi-info-circle-fill"></i> {videoResult.disclaimer}
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="alert alert-danger">
              <i className="bi bi-exclamation-triangle-fill"></i> {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoParser;
