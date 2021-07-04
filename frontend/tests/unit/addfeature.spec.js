import { shallowMount } from '@vue/test-utils'
import AddFeature from '@/components/AddFeature.vue'

describe('AddFeature.vue', () => {
  const wrapper = shallowMount(AddFeature);

  it('renders', () => {
    expect(wrapper.exists()).toBe(true);
  })

  it('contains button', () => {
    expect(wrapper.find('button').exists()).toBe(true);
    expect(wrapper.find('button').text()).toBe('Submit');
  })

  it('has an add feature with data', () => {
    wrapper.find('input').setValue('New Test Feature')
    wrapper.find('textarea').setValue('Test Feature Description')
    wrapper.find('input[type=radio][value=Values]').setChecked(true)
    wrapper.find('input[type=radio][value=Principles]').setChecked()
    wrapper.find('button').trigger('click')
  })

  it('has an add feature without data', () => {
    wrapper.find('button').trigger('click')
  })

})


