import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
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
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
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
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
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
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
            ]),
      ]),
      BackgroundSectionModel(
          title: t.homeView.styles.smart_tool.title,
          cardHeight: 160,
          items: [
            StyleModel(
              url: 'https://zeerk.com/storage/uploads/2023/07/1-1.jpg',
              title: t.homeView.styles.smart_tool.types.remove_background,
              subTitle: '6 ${t.profile.photos}',
              data: ['Description', 'Description', 'Description'],
              actionTitle: t.common.next,
              onTap: (model) {
                router.goNamed(AppViews.toolsView,
                    extra: {'model': model, 'isRemoveBackground': true});
              },
              description:
                  'This style is suitable for showing in a business style to show all your inner qualities',
            ),
            StyleModel(
              url:
                  'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              title: t.homeView.styles.smart_tool.types.enhance,
              subTitle: '6 ${t.profile.photos}',
              actionTitle: t.common.next,
              data: ['Description', 'Description', 'Description'],
              onTap: (model) {
                router.goNamed(AppViews.enhanceView, extra: {'model': model});
              },
              description:
                  'This style is suitable for showing in a business style to show all your inner qualities',
            ),
            StyleModel(
              url:
                  'https://humple.club/uploads/posts/2022-11/1668592044_34-humple-club-p-strizhka-pryamoe-kare-zhenskie-oboi-34.jpg',
              title: t.homeView.styles.smart_tool.types.remove_objects,
              subTitle: '6 ${t.profile.photos}',
              actionTitle: t.common.next,
              onTap: (model) {
                router.goNamed(AppViews.toolsView,
                    extra: {'model': model, 'isRemoveBackground': false});
              },
              data: ['Description', 'Description', 'Description'],
              description:
                  'This style is suitable for showing in a business style to show all your inner qualities',
            ),
          ]),
    ];

    return Provider(
        create: (context) =>
            PacksStore(restClient: context.read<Dependencies>().restClient),
        builder: (context, _) {
          final PacksStore store = Provider.of<PacksStore>(context);

          return Scaffold(
            body: AppBody(
              builder: (windowWidth, windowHeight, windowSize) {
                return CustomScrollView(
                  slivers: [
                    SliverToBoxAdapter(
                      child: AppBarHomeView(
                        model: sections[0].items[1],
                      ),
                    ),
                    SliverPadding(
                        padding: HorizontalSpacing.centered(windowWidth) +
                            const EdgeInsets.only(top: AppValues.kPadding),
                        sliver: SliverToBoxAdapter(
                          child: SearchBarWidget(),
                        )),
                    SliverToBoxAdapter(
                      child: HomeBody(store: store, windowWidth: windowWidth),
                    )
                  ],
                );
              },
            ),
          );
        });
  }
}
