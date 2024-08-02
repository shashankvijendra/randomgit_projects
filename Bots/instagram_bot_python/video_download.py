from instaloader import Instaloader, Profile

def download_video(username):
    L = Instaloader(download_pictures=False)
    PROFILE = username
    profile = Profile.from_username(L.context, PROFILE)

    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes,reverse=True)
    print(len(posts_sorted_by_likes))
    for post in posts_sorted_by_likes:
        if post.is_video:
            L.download_post(post, PROFILE)

import instaloader
# Download the video
def instagram_download_video(post_url, username):
    try:
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False
        )
        post = instaloader.Post.from_shortcode(loader.context, post_url.split('/')[-2])
        if post.is_video:
            loader.download_post(post, target=username)
            print("Video downloaded successfully.")
        else:
            print("The post is not a video.")
    except Exception as e:
        print(f"An error occurred: {e}")

instagram_download_video("https://www.instagram.com/p/C-C_3Tri_SC/", "name")