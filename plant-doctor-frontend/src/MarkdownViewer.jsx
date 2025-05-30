import ReactMarkdown from 'react-markdown';

function MarkdownViewer({ content }) {
  return (
    <div className="prose">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}

export default MarkdownViewer;
