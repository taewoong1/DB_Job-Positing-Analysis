document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('checkPage').addEventListener('click', async function () {
      let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      const url = tab.url; // Get URL of the current tab
      console.log('URL:', url);

      try {
          const response = await fetch('http://localhost:5000/send_url', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ url: url })
          });

          if (response.ok) {
              const blob = await response.blob();
              const imgUrl = '/mnt/data/visualization.png'
              const imgElement = document.getElementById('displayImage');
              imgElement.src = imgUrl;
              imgElement.hidden = false;  // Display the image
          } else {
              console.error('Failed to fetch image:', response.statusText);
          }
      } catch (error) {
          console.error('Error fetching the image:', error);
      }
  });
});
