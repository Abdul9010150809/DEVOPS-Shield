import React, { useEffect } from 'react';
import './NotificationSystem.css';

const NotificationSystem = ({ notifications, onRemove }) => {
  useEffect(() => {
    // Auto-remove notifications after their duration
    const timers = notifications.map(notification => {
      if (notification.duration) {
        return setTimeout(() => {
          onRemove(notification.id);
        }, notification.duration);
      }
      return null;
    });

    return () => {
      timers.forEach(timer => timer && clearTimeout(timer));
    };
  }, [notifications, onRemove]);

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
      default:
        return 'ℹ️';
    }
  };

  const getNotificationClass = (type) => {
    return `notification notification-${type}`;
  };

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="notification-system" aria-live="polite" aria-atomic="true">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={getNotificationClass(notification.type)}
          role="alert"
          aria-label={`${notification.type} notification: ${notification.message}`}
        >
          <div className="notification-content">
            <span className="notification-icon" aria-hidden="true">
              {getNotificationIcon(notification.type)}
            </span>
            <div className="notification-message">
              <p>{notification.message}</p>
              {notification.timestamp && (
                <span className="notification-time">
                  {new Date(notification.timestamp).toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>
          <button
            className="notification-close"
            onClick={() => onRemove(notification.id)}
            aria-label={`Dismiss ${notification.type} notification`}
            title="Dismiss notification"
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>
      ))}
    </div>
  );
};

export default NotificationSystem;
