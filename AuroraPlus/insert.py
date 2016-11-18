from models import LandingPageImages

image = LandingPageImages(
    PictureLinkName="image1",
    PictureLink="http://imgur.com/Sdy6Vq0.png",
    DescText="Clean overview of all your servers and all the necessary data you need. "
             "We designed it to be clean, understandable and modern looking."
)

image.save()

image2 = LandingPageImages(
    PictureLinkName="image2",
    PictureLink="http://imgur.com/VgE7yXo.png",
    DescText="In the dashboard menu you can choose the server you want to see. "
             "In this case server 1, server 2 en server 3."
)

image2.save()

image3 = LandingPageImages(
    PictureLinkName="image3",
    PictureLink="http://imgur.com/qIxUbVi.png",
    DescText="Once on the server page, the details are displayed in the graphics. "
             "Monitoring your servers was never this easy!"
)

image3.save()
