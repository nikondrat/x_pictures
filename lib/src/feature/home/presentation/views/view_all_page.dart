import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/data.dart';

class ViewAllPage extends StatelessWidget {
  const ViewAllPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(textName: 'Linkedin'),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: .8,
            mainAxisSpacing: 15,
            crossAxisSpacing: 15,
          ),
          itemCount: 10,
          itemBuilder: (BuildContext context, int index) {
            return const ImageItemViewAllPage();
          },
        ),
      ),
    );
  }
}
