const xqueryApp = Vue.createApp({
    data() {
        return {
            query: '',
            results: null,
            error: null,
        };
    },
    methods: {
        async runQuery() {
            try {
                this.results = null; // Reset results
                this.error = null;   // Reset errors

                const response = await axios.post('/api/xquery', {
                    query: this.query,
                });

                this.results = response.data.results;
            } catch (error) {
                console.error(error);
                this.error = 'An error occurred while processing your query.';
            }
        },
    },
});

xqueryApp.mount('#app');
