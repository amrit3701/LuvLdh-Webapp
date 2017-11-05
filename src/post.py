import facebook

def main():
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : "126210538066873",  # Step 1
    "access_token" : "EAACEdEose0cBALgZCtZBWBLgeVPmaZA1REphjpaHW2zspo4aeVrnvjsI2IpWXsO7LCZA991QnzQjSxY6zEFCbpkIdQY3QSkN3ARamLfZCDeysr7u9S5I0F0KyxYLpamwsjfZCyZAH1Gh5VHzy4H3JJ4ZCZCvqFZCqmtaPSVIDPqhZALG8a7F8KE2yphOVgA8su7wBYZD"   # Step 3
    }

  api = get_api(cfg)
  msg = "no time"
  attachment =  {
       # 'name': 'Link name'
      'link': 'https://www.facebook.com/amrit3701/posts/1542404899173604'#'https://www.facebook.com/permalink.php?story_fbid=686531618207438&id=100005518185417'
       # 'caption': 'Check out this example',
       # 'description': 'This is a longer description of the attachment',
       # 'picture': 'https://www.example.com/thumbnail.jpg'
    }
  print attachment['link']
  status = api.put_wall_post(msg,attachment)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip
  # the following if you want to post as yourself.
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()
