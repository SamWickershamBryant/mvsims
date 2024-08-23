const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
};

const ctx = document.getElementById('myChart').getContext('2d');
const simChart = new Chart(ctx, {
    type: 'line',
    
    options: {
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'minute',
            displayFormats: {
                minute: 'DD T'
            },
            tooltipFormat: 'DD T'
          },
          title: {
            display: true,
            text: 'Timestamp'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Data Usage (GB)'
          }
        }
      }
    }
  });


document.addEventListener('DOMContentLoaded', function() {
    $('#thing-select').select2();
    const thingSelect = document.getElementById('thing-select')
    let allThings = []
    let populated = false

    const fetchData = async () => {
        try {
            const response = await fetch(window.location.href + 'usages');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            allThings = [...new Set(data.map(item => item.thing))];
            
            const mostRecentTs = Math.max(...data.map(item => new Date(item.ts)));

            const recentData = data.filter(item => new Date(item.ts).getTime() === mostRecentTs);

            const totalDataUsage = recentData.reduce((sum, item) => sum + item.data, 0);
            totalUsage = document.getElementById('totalUsage')
            totalUsage.style = "color:red;"
            totalUsage.innerHTML = totalDataUsage.toFixed(2)
            
            if (!populated){
              populateThingSelect(allThings)
              populated = true
            }
            
            filterAndDisplay(data);
            
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const populateThingSelect = (things) => {
      things.forEach(thing => {
        const option = document.createElement('option');
            option.value = thing;
            option.text = thing;
            option.id = thing;
            thingSelect.add(option);
      })
    }

    const filterAndDisplay = (data) => {
      const fromDate = document.getElementById('from-date').value;
        const toDate = document.getElementById('to-date').value;
        const selectedThings = Array.from(thingSelect.selectedOptions).map(option => option.value);
        console.log(thingSelect)

        const filteredData = data.filter(item => {
          const itemDate = new Date(item.ts);
          const dateFilter = (!fromDate || itemDate >= new Date(fromDate)) &&
                             (!toDate || itemDate <= new Date(toDate));
          const thingFilter = (selectedThings.length === 0 || selectedThings.includes(item.thing));
          return dateFilter && thingFilter;
      });
  
      updateChart(filteredData);
    }

    const updateChart = (data) => {
        
        
        // Extract unique things
        const things = [...new Set(data.map(item => item.thing))];
        
        // Prepare datasets for each thing
        const datasets = things.map(thing => {
            return {
                label: thing,
                data: data.filter(item => item.thing === thing).map(item => ({
                    x: new Date(item.ts),
                    y: item.data
                })),
                fill: false,
                borderColor: getRandomColor(),
                tension: 0.1
            };
        });
        console.log(datasets)

        simChart.data.datasets = datasets
        simChart.update()
    
        
    };
  
    

    const updateUsagesContainer = (data) => {
        const container = document.getElementById('usages-container');
        container.innerHTML = '';
        data.forEach(usage => {
            const usageElement = document.createElement('div');
            usageElement.innerHTML = `
                <h3>THING: ${usage.thing}</h3>
                <p>data: ${usage.data}</p>
                <p>time: ${new Date(usage.ts).toLocaleString()}</p>
            `;
            container.appendChild(usageElement);
        });
    };

    document.getElementById('refresh-button').addEventListener('click', fetchData);

    // Initial fetch
    fetchData();
});