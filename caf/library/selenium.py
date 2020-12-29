#!/usr/bin/python

# Copyright: (c) 2020, Kevin Thomas <kevin@mytechnotalent.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: selenium

short_description: Selenium module.

version_added: "1.0"

description:
    - "Selenium module which allows you to perform headless Selenium within Ansible."

options:
    query:
        description:
            - This is the query string to search with a page's search box.
        required: true
    url:
        description:
            - This is the url for the Selenium driver to visit.
        required: true
    find_element_by :
        description:
            - This is the find_element_by option such as id, name, xpath, etc.
        required: true
    element:
        description:
            - The element to query on a page.
        required: true

extends_documentation_fragment:t
    - (none)

author:
    - Kevin Thomas (@mytechnotalent)
'''

EXAMPLES = '''
# Pass in a message
- name: Test selenium
  selenium:
    query: 'twitter'
    url: 'google.com'
    find_element_by: 'name'
    element: 'q'
  register: test
  vars:
    ansible_python_interpreter: '/usr/bin/python3'
'''

RETURN = '''
element_result:
    description: The page element_result.
    type: str
    returned: always
'''


from ansible.module_utils.basic import AnsibleModule

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def launch():
    # allocate headless driver object
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1024x768')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    return driver


def run_module(module):
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    query = module.params['query']
    url = module.params['url']
    find_element_by = module.params['find_element_by']
    element = module.params['element']

    try:
        driver = launch()
        driver.get('https://{}'.format(url))
        if find_element_by == 'id':
            element_result = driver.find_element_by_id('{}'.format(element))
        if find_element_by == 'name':
            element_result = driver.find_element_by_name('{}'.format(element))
        if find_element_by == 'xpath':
            element_result = driver.find_element_by_xpath('{}'.format(element))
        element_result.send_keys(query)
        element_result.send_keys(Keys.RETURN)
        element_result = driver.find_element_by_xpath('//*').text
        driver.quit()
    except:
        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        driver.quit()
        module.fail_json(msg='Can\'t locate element.')

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        element_result=element_result
    )

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(result=result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        query=dict(type='str', required=True),
        url=dict(type='str', required=True),
        find_element_by=dict(type='str', required=True),
        element=dict(type='str', required=True)
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args
    )

    run_module(module)


if __name__ == '__main__':
    main()
