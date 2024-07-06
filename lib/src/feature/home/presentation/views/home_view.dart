import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    final List<BackgroundSectionModel> sections = [
      BackgroundSectionModel(title: t.homeView.styles.linkedin.title, items: [
        StyleModel(
            url:
                'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
            title: t.homeView.styles.linkedin.styles.streetCasual,
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            subTitle: '6 ${t.profile.photos}',
            data: [
              'Description',
              'Description',
              'Description'
            ],
            images: [
              'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
              'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
              'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
              'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg'
            ]),
        StyleModel(
            url:
                'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
            title: t.homeView.styles.linkedin.styles.office,
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            subTitle: '6 ${t.profile.photos}',
            data: [
              'Description',
              'Description',
              'Description'
            ],
            images: [
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
            ]),
        StyleModel(
            url:
                'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
            title: t.homeView.styles.linkedin.styles.streetCasual,
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            subTitle: '6 ${t.profile.photos}',
            data: [
              'Description',
              'Description',
              'Description'
            ],
            images: [
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
            ]),
        StyleModel(
            url:
                'https://i.pinimg.com/originals/e8/99/05/e89905c4d9f7108cde6e4982e47baab1.jpg',
            title: t.homeView.styles.linkedin.styles.notebook,
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            subTitle: '6 ${t.profile.photos}',
            data: [
              'Description',
              'Description',
              'Description'
            ],
            images: [
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
              'https://i.pinimg.com/736x/92/ee/c0/92eec00db6ec4b688f045e2b035279cd--interesting-faces-facial-hair.jpg',
            ]),
      ]),
      BackgroundSectionModel(title: t.homeView.styles.hairStyle.title, items: [
        StyleModel(
            url:
                'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
            title: t.homeView.styles.hairStyle.styles.bobCut,
            subTitle: '6 ${t.profile.photos}',
            data: ['Description', 'Description', 'Description'],
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            images: [
              'https://images.glavred.info/2019_10/thumb_files/1200x0/1570396895-1764.jpg',
              'https://www.ewparik.com/upload/resize_cache/iblock/56a/1200_1200_1fa72c7c719b9bf5d96a98e09d4c1005a/3h03d42ar041tzveazrh5qsnpg11giwd.jpg'
            ]),
        StyleModel(
            url:
                'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
            title: t.homeView.styles.hairStyle.styles.green,
            subTitle: '6 ${t.profile.photos}',
            data: ['Description', 'Description', 'Description'],
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            images: [
              'https://images.glavred.info/2019_10/thumb_files/1200x0/1570396895-1764.jpg',
              'https://www.ewparik.com/upload/resize_cache/iblock/56a/1200_1200_1fa72c7c719b9bf5d96a98e09d4c1005a/3h03d42ar041tzveazrh5qsnpg11giwd.jpg'
            ]),
        StyleModel(
            url:
                'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
            title: t.homeView.styles.hairStyle.styles.pink,
            subTitle: '6 ${t.profile.photos}',
            data: ['Description', 'Description', 'Description'],
            description:
                'This style is suitable for showing in a business style to show all your inner qualities',
            images: [
              'https://images.glavred.info/2019_10/thumb_files/1200x0/1570396895-1764.jpg',
              'https://www.ewparik.com/upload/resize_cache/iblock/56a/1200_1200_1fa72c7c719b9bf5d96a98e09d4c1005a/3h03d42ar041tzveazrh5qsnpg11giwd.jpg'
            ]),
      ]),
    ];

    return Scaffold(
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return CustomScrollView(
            slivers: [
              const SliverToBoxAdapter(
                child: AppBarHomeView(),
              ),
              SliverPadding(
                padding: HorizontalSpacing.centered(windowWidth),
                sliver: SliverList.list(
                    children: sections.map((e) {
                  return BackgroundSection(
                    section: e,
                    onTap: (model) {
                      router.goNamed(AppViews.officePageRoute, extra: {
                        'model': model,
                      });
                    },
                  );
                }).toList()),
              )
            ],
          );
        },
      ),
    );
  }
}
