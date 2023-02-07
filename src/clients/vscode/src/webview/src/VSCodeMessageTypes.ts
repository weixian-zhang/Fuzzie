export interface SaveFileMessage {
  command: 'save-file';
  filename: string;
  content: string
}

export interface LogMessage {
    command: 'log';
    message: string
}
