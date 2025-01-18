  document.getElementById('input-form').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const topic = document.getElementById('topic').value;
    const proResultsDiv = document.getElementById('pro-results');
    const antiResultsDiv = document.getElementById('anti-results');
  
    proResultsDiv.innerHTML = 'Loading pro articles...';
    antiResultsDiv.innerHTML = 'Loading anti articles...';

    const proSidePhrase = `support for ${topic}, ${topic} benefits, ${topic} positive effects`;
    const antiSidePhrase = `opposition to ${topic}, ${topic} risks, ${topic} negative effects`;
  
    try {
      const proResponse = fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, side: proSidePhrase }),
      });
  
      const antiResponse = fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, side: antiSidePhrase }),
      });

      const [proData, antiData] = await Promise.all([proResponse, antiResponse].map(res => res.then(r => r.json())));
  
      proResultsDiv.innerHTML = '<h2>Pro Articles</h2>';
      proData.articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.innerHTML = `
          <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
          <p>${article.snippet}</p>
        `;
        proResultsDiv.appendChild(articleDiv);
      });
  
      antiResultsDiv.innerHTML = '<h2>Anti Articles</h2>';
      antiData.articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.innerHTML = `
          <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
          <p>${article.snippet}</p>
        `;
        antiResultsDiv.appendChild(articleDiv);
      });
    } catch (error) {
      proResultsDiv.innerHTML = `<p style="color: red;">Error fetching pro articles: ${error.message}</p>`;
      antiResultsDiv.innerHTML = `<p style="color: red;">Error fetching anti articles: ${error.message}</p>`;
    }
});