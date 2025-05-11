import { mount } from '@vue/test-utils';
import { describe, expect, beforeEach, test, vi } from 'vitest';
import AboutPage from '../src/views/AboutView.vue';
import HomePage from '../src/views/HomeView.vue';
import router from '../src/router/index.js';

describe('Router Tests', () => {
    beforeEach(async () => {
        await router.push('/');
        await router.isReady();
    });

    test('about page router', async () => {
        await router.push('/about');
        await router.isReady();

        const wrapper = mount(AboutPage, {
            global: {
                plugins: [router]
            }
        });

        expect(router.currentRoute.value.path).toBe('/about');
        expect(wrapper.find('h2').text()).toContain('Aberdeen Burgh Registers');
    });

    test('home page router', async () => {
        await router.push('/');
        await router.isReady();

        const wrapper = mount(HomePage, {
            global: {
                plugins: [router]
            }
        });

        expect(router.currentRoute.value.path).toBe('/');
        expect(wrapper.find('h1').text()).toContain('Discover 7 Volumes');
    });

    test('search page router', async () => {
        await router.push({
            path: '/search',
            query: {
                query_type: 'basic_search',
                caseSensitive: false,
                basicSearch: 'holly',
                methodSearch: 'word_start',
                language: 'any',
                variant: '0',
                pageSearch: '',
                entrySearch: '',
                startDate: '',
                endDate: '',
                docId: '',
                resultsPerPage: '10',
                sortBy: 'frequency'
            }
        });

        await router.isReady();

        expect(router.currentRoute.value.path).toBe('/search');
        // tests if the query parameters are set correctly
        expect(router.currentRoute.value.query).toMatchObject({
            query_type: 'basic_search',
            basicSearch: 'holly',
            methodSearch: 'word_start',
        });
        // test url
        expect(router.currentRoute.value.fullPath).toBe('/search?query_type=basic_search&caseSensitive=false&basicSearch=holly&methodSearch=word_start&language=any&variant=0&pageSearch=&entrySearch=&startDate=&endDate=&docId=&resultsPerPage=10&sortBy=frequency');
    });

});