import { shallowMount } from '@vue/test-utils'
import Dashboard from '@/components/Dashboard.vue'

describe('Dashboard.vue', () => {
  const wrapper = shallowMount(Dashboard);

  it('renders', () => {
    expect(wrapper.exists()).toBe(true);
  })

  it('contains h2', () => {
    expect(wrapper.find('h2').text()).toBe('Agile Software Development');
  })

  it('has a table', () => {
    expect(wrapper.find('table').exists()).toBe(true);
  })

})


