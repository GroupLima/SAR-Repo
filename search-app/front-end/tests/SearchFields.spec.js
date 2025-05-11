import { shallowMount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { nextTick } from 'vue'
import SearchFields from '@/components/SearchFields.vue'
import router from '@/router'

describe('SearchFields', () => {
  let wrapper
  let mockRouter

  beforeEach(() => {
    vi.clearAllMocks()
    mockRouter = {
      push: vi.fn()
    }

    wrapper = shallowMount(SearchFields, {
      global: {
        plugins: [router],
        mocks: {
          $router: mockRouter
        }
      }
    })
  })

  it('default advanced search values', () => {
    expect(wrapper.vm.form.query_type).toBe('basic_search')
    expect(wrapper.vm.form.methodSearch).toBe('keywords')
    expect(wrapper.vm.form.language).toBe('any')
    expect(wrapper.vm.form.resultsPerPage).toBe(10)
    expect(wrapper.vm.form.sortBy).toBe('frequency')
  })

  it('update search when input changes', async () => {
    const searchInput = wrapper.find('#search-box')
    await searchInput.setValue('test query')
    expect(wrapper.vm.form.basicSearch).toBe('test query')
  })

  it('toggle advanced search dropdown', async () => {
    const dropdownButton = wrapper.find('.dropdown-button')
    expect(wrapper.vm.isDropdownOpen).toBe(false)
    await dropdownButton.trigger('click')
    expect(wrapper.vm.isDropdownOpen).toBe(true)
    await dropdownButton.trigger('click')
    expect(wrapper.vm.isDropdownOpen).toBe(false)
  })

  it('toggle all volumes', async () => {
    // open dropdown
    await wrapper.find('.dropdown-button').trigger('click')
    await nextTick()

    // default - no volumes
    expect(wrapper.vm.form.volumes.length).toBe(0)

    // click all volumes button
    await wrapper.vm.toggleAllVolumes()
    expect(wrapper.vm.form.volumes).toEqual(['1', '2', '4', '5', '6', '7', '8'])

    // click all volumes button again
    await wrapper.vm.toggleAllVolumes()
    expect(wrapper.vm.form.volumes).toEqual([])
  })
})