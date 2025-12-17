document.addEventListener('DOMContentLoaded', () => {
    const verifyBtn = document.getElementById('verifyBtn');
    const scanningOverlay = document.querySelector('.scanning-overlay');
    const visualizerText = document.querySelector('.placeholder-text');
    const resultsContainer = document.getElementById('resultsContainer');
    const refreshChainBtn = document.getElementById('refreshChain');

    // UI Elements for result
    const statusVal = document.getElementById('statusValue');
    const coverVal = document.getElementById('coverValue');
    const confidVal = document.getElementById('confidenceValue');
    const ledgerFeed = document.getElementById('ledgerFeed');

    verifyBtn.addEventListener('click', async () => {
        const lat = document.getElementById('latInput').value;
        const lon = document.getElementById('lonInput').value;

        // Start UI Loading State
        scanningOverlay.classList.remove('hidden');
        visualizerText.textContent = "Acquiring Satellite Lock...";
        verifyBtn.disabled = true;

        try {
            const response = await fetch('/api/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lon })
            });
            const data = await response.json();

            // Simulate processing delay for effect
            setTimeout(() => {
                scanningOverlay.classList.add('hidden');
                visualizerText.textContent = "Scan Complete.";
                verifyBtn.disabled = false;

                updateResults(data.verification);
                updateLedger(); // Refresh ledger
            }, 1500);

        } catch (error) {
            console.error(error);
            visualizerText.textContent = "Error: Connection Failed";
            scanningOverlay.classList.add('hidden');
            verifyBtn.disabled = false;
        }
    });

    refreshChainBtn.addEventListener('click', updateLedger);

    function updateResults(data) {
        statusVal.textContent = data.status;
        statusVal.setAttribute('data-status', data.status);
        coverVal.textContent = data.green_cover_percentage + '%';
        confidVal.textContent = data.ai_confidence + '%';

        // Update the Reason Field
        const reasonEl = document.getElementById('reasonValue');
        if (data.reasons && data.reasons.length > 0) {
            reasonEl.textContent = data.reasons.join(' | ');
            reasonEl.style.color = data.status === 'VERIFIED' ? '#4CAF50' : '#ff6b6b';
        } else {
            reasonEl.textContent = 'Analysis Complete';
            reasonEl.style.color = '#aaa';
        }
    }

    async function updateLedger() {
        try {
            const response = await fetch('/api/chain');
            const data = await response.json();

            ledgerFeed.innerHTML = '';

            // Reverse to show newest first
            [...data.chain].reverse().forEach(block => {
                const item = document.createElement('div');
                item.className = 'ledger-item';

                // Format nicely
                const hashShort = block.previous_hash.substring(0, 10) + '...';
                const time = block.timestamp;
                const dataCount = block.data.length;

                item.innerHTML = `
                    <span style="color: #555;">[${time}]</span> 
                    <strong>Block #${block.index}</strong> 
                    | PrevHash: ${hashShort} 
                    | Data: verification_data
                `;
                ledgerFeed.appendChild(item);
            });
        } catch (e) {
            console.error(e);
        }
    }

    // Initial load
    updateLedger();
});
