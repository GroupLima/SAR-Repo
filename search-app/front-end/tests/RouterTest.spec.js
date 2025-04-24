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

    test('about page router test', async () => {
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

    test('search function test', async () => {
        await router.push({
            path: '/search',
            query: {
                query_type: 'basic_search',
                basicSearch: 'holly',
                methodSearch: 'word_start'
            }
        });

        await router.isReady();

        expect(router.currentRoute.value.path).toBe('/search');
        expect(router.currentRoute.value.query).toMatchObject({
            query_type: 'basic_search',
            basicSearch: 'holly',
            methodSearch: 'word_start',
        });
    });

});