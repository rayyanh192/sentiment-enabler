/*
document.getElementById('input-form').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const topic = document.getElementById('topic').value;
    const side = document.getElementById('side').value;
  
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading...';
  
    try {
      const response = await fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, side }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch data from the backend');
      }
  
      const data = await response.json();
  
      // Display the results
      resultsDiv.innerHTML = '';
      data.articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.innerHTML = `
          <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
          <p>${article.snippet}</p>
        `;
        resultsDiv.appendChild(articleDiv);
      });
    } catch (error) {
      resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });*/
  document.getElementById('input-form').addEventListener('submit', async function (event) {
    event.preventDefault();
  
    const topic = document.getElementById('topic').value;
    const proResultsDiv = document.getElementById('pro-results');
    const antiResultsDiv = document.getElementById('anti-results');
  
    proResultsDiv.innerHTML = 'Loading pro articles...';
    antiResultsDiv.innerHTML = 'Loading anti articles...';
  
    try {
      const proResponse = fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, side: `pro-${topic}` }),
      });
  
      const antiResponse = fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, side: `anti-${topic}` }),
      });

      // Await both responses simultaneously
      const [proData, antiData] = await Promise.all([proResponse, antiResponse].map(res => res.then(r => r.json())));
  
      // Display pro articles
      proResultsDiv.innerHTML = '';
      proData.articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.innerHTML = `
          <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
          <p>${article.snippet}</p>
        `;
        proResultsDiv.appendChild(articleDiv);
      });
  
      // Display anti articles
      antiResultsDiv.innerHTML = '';
      antiData.articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.innerHTML = `
          <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
          <p>${article.snippet}</p>
        `;
        antiResultsDiv.appendChild(articleDiv);
      });
    } catch (error) {
      proResultsDiv.innerHTML = `<p>Error fetching pro articles: ${error.message}</p>`;
      antiResultsDiv.innerHTML = `<p>Error fetching anti articles: ${error.message}</p>`;
    }
  });