import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SearchResults from '../src/components/SearchResults.vue'
import SearchResultCard from '../src/components/SearchResultCard.vue'
import axios from 'axios'
global.scrollTo = vi.fn()

// creates a mock of axios
vi.mock('axios')

// mock data of search result params and response
describe('SearchResults', () => {
    const mockQueryParams = { query: 'test search' }
    const mockSearchResponse = {
        data: {
            success: true,
            results: {
                "ARO-1-0001-01": { 
                    highlighted_html: 'test result', 
                    volume: '1', 
                    page: '0001', 
                    date: '1398-09-30'
                },
            },
            total_results: 10
        }
    }

    // clear all mocks before each test
    beforeEach(() => { vi.clearAllMocks() })

    // test if search results are displayed
    it('displays search results', async () => {
        axios.get.mockResolvedValue(mockSearchResponse)
        const wrapper = mount(SearchResults, {
            props: { queryParams: mockQueryParams }
        })

        await wrapper.vm.$nextTick()
        expect(axios.get).toHaveBeenCalled()
        await wrapper.vm.$nextTick()
        expect(wrapper.text()).toContain('test result')
    })

    // tests page changing
    it('page changing', async () => {
        axios.get.mockResolvedValue(mockSearchResponse)
        const wrapper = mount(SearchResults, {
            props: { queryParams: mockQueryParams },
            global: { components: { SearchResultCard } }
        })

        await wrapper.vm.$nextTick()
        expect(axios.get).toHaveBeenCalled()
        await wrapper.vm.$nextTick()

        // identify the next and previous buttons and make sure they exist
        const buttons = wrapper.findAll('button')
        const nextButton = buttons.find(button => button.text() === 'Next')
        const prevButton = buttons.find(button => button.text() === 'Previous')
        expect(nextButton.exists()).toBe(true)
        expect(prevButton.exists()).toBe(true)

        // test next page button
        await nextButton.trigger('click')
        expect(wrapper.vm.state.current_page).toBe(2)

        // test previous page button
        await prevButton.trigger('click')
        expect(wrapper.vm.state.current_page).toBe(1)
    })
})