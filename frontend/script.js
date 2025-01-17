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
  });