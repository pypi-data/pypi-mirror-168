export default function main() {
  return {
    name: 'remove-plotly-script-tag',
    enforce: 'pre',
    apply: 'build',
    transformIndexHtml(html: string) {
      console.log('test-------------------');

      return html.replace(/<script(.*?plotly.+?)<\/script>/, '')
    },

  };
}