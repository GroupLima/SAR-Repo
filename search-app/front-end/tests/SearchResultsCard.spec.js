import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SearchResultCard from '@/components/SearchResultCard.vue'

const mockClipboard = {
    writeText: vi.fn()
};

Object.defineProperty(global.navigator, 'clipboard', {
    value: mockClipboard,
    writable: true,
});

describe('SearchResultCard Component', () => {
    it('renders result data correctly', () => {
        const wrapper = mount(SearchResultCard, {
            props: {
                id: 'ARO-1-0001-01',
                htmlContent: 'test result',
                htmlvolume: '1',
                htmlpage: '0001',
                date: {
                    when: '1398-09-30',
                    certainty: 'high'
                },
                htmllang: 'Latin'
            }
        });

        // test to see if all of the information is displayed
        expect(wrapper.html()).toContain('test result')
        expect(wrapper.html()).toContain('Volume: 1')
        expect(wrapper.html()).toContain('Page: 0001')
        expect(wrapper.html()).toContain('Date: 1398-09-30')
        expect(wrapper.html()).toContain('Language: Latin')
    })
});

describe('SearchResultCard Buttons', () => {
    beforeEach(() => {
        mockClipboard.writeText.mockClear()
    });

    it('copy button test', () => {
        const wrapper = mount(SearchResultCard, {
            props: {
                id: 'ARO-1-0001-01',
                htmlContent: 'test result',
                htmlvolume: '1',
                htmlpage: '0001',
                date: {
                    when: '1398-09-30',
                    certainty: 'high'
                },
                htmllang: 'Latin'
            }
        });

        const copyButton = wrapper.find('button[title="Copy text"]')
        expect(copyButton.exists()).toBe(true)
        copyButton.trigger('click')
        // test if the htmlContent is copied to the clipboard
        expect(mockClipboard.writeText).toHaveBeenCalledWith('test result')
    });
});