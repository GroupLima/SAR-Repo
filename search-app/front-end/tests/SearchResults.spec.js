import { mount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import SearchResults from '../src/components/SearchResults.vue'
import SearchResultCard from '../src/components/SearchResultCard.vue'
import axios from 'axios'
import router from '@/router'
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

describe('SearchResults components', () => {
    let wrapper
    let mockQueryParams
    let mockSearchResponse

    beforeEach(() => {
        vi.clearAllMocks()

        mockQueryParams = {
            query_type: 'basic_search',
            basicSearch: 'test search',
            methodSearch: 'keywords',
            resultsPerPage: 10,
            sortBy: 'frequency'
        }

        mockSearchResponse = {
            data: {
                success: true,
                results: {
                    "ARO-1-0001-01": {
                        highlighted_html: 'test result',
                        volume: '1',
                        page: '0001',
                        date: '1398-09-30',
                        lang: 'latin'
                    },
                    "ARO-1-0002-01": {
                        highlighted_html: 'another test',
                        volume: '1',
                        page: '0002',
                        date: '1398-10-02',
                        lang: 'latin'
                    }
                },
                num_results: 10,
                total_results: 17,
                variant: 0
            }
        }

        axios.get.mockResolvedValue(mockSearchResponse)
    })

    it('displays search results', async () => {
        wrapper = mount(SearchResults, {
            props: { queryParams: mockQueryParams },
            global: {
                stubs: {
                    SearchResultCard: true
                },
                mocks: {
                    $router: router
                }
            }
        })

        await flushPromises()

        expect(axios.get).toHaveBeenCalledWith('/api/search', {
            params: expect.objectContaining({
                basicSearch: 'test search',
                methodSearch: 'keywords'
            })
        })

        expect(wrapper.text()).toContain('Showing 1 to 10 of 17 entries')
    })

    it('calculates correct page numbers', async () => {
        mockSearchResponse.data.total_results = 50

        wrapper = mount(SearchResults, {
            props: { queryParams: mockQueryParams },
            global: {
                stubs: {
                    SearchResultCard: true
                },
                mocks: {
                    $router: router
                }
            }
        })

        await flushPromises()

        // 50 results, 10 per page
        expect(wrapper.vm.state.total_pages).toBe(5)
        expect(wrapper.vm.displayedPageNumbers.length).toBe(5)
    })

    it('calculates correct first and last result', async () => {
        mockSearchResponse.data.total_results = 25

        wrapper = mount(SearchResults, {
            props: { queryParams: mockQueryParams },
            global: {
                stubs: {
                    SearchResultCard: true
                },
                mocks: {
                    $router: router
                }
            }
        })

        await flushPromises()

        // page 1
        expect(wrapper.vm.firstResultOfPage).toBe(1)
        expect(wrapper.vm.lastResultOfPage).toBe(10)

        // page 2
        await wrapper.vm.selectedPage(2)
        expect(wrapper.vm.firstResultOfPage).toBe(11)
        expect(wrapper.vm.lastResultOfPage).toBe(20)

        // page 3 (last 5 results)
        await wrapper.vm.selectedPage(3)
        expect(wrapper.vm.firstResultOfPage).toBe(21)
        expect(wrapper.vm.lastResultOfPage).toBe(25)
    })
})